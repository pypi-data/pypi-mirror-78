import pytest
from itertools import product


@pytest.fixture(
    params=list(product([-3.0, -2.9], [1.5, 1.6])), autouse=True, scope="function"
)
def fake_data(request):
    import numpy as np

    beta_s, beta_d = request.param

    nfreq = 12
    sens = 2
    npix = 100

    dust_template = 100.0 * np.ones((1, 2, npix))
    freq_d = 353.0
    T_d = 20.0

    sync_template = 5 * np.ones((1, 2, npix))
    freq_s = 23.0

    cmb_template = 10.0 * np.ones((1, 2, npix))

    freq_obs = np.array(
        [23.0, 30.0, 40.0, 95.0, 100.0, 145.0, 220.0, 270.0, 300.0, 353.0, 545, 800]
    )
    assert len(freq_obs) == nfreq
    sensitivities = np.array([sens] * nfreq)

    hnkt_ref = 0.0479924466 * freq_d / T_d
    dust_fn = (
        lambda nu: (nu / freq_d) ** (beta_d + 1)
        * (np.exp(hnkt_ref) - 1)
        / (np.exp(0.0479924466 * nu / T_d) - 1)
    )
    sync_fn = lambda nu: (nu / freq_s) ** (beta_s)
    cmb_fn = (
        lambda nu: np.exp(0.0176086761 * nu)
        * (0.0176086761 * nu / (np.exp(0.0176086761 * nu) - 1)) ** 2
    )

    dust_scaling = np.array(list(map(dust_fn, freq_obs)))
    dust_scaled = dust_scaling[:, None, None] * dust_template

    sync_scaling = np.array(list(map(sync_fn, freq_obs)))
    sync_scaled = sync_scaling[:, None, None] * sync_template

    cmb_scaling = np.array(list(map(cmb_fn, freq_obs)))
    cmb_scaled = cmb_scaling[:, None, None] * cmb_template

    data = dust_scaled + cmb_scaled + sync_scaled
    covariance = np.ones((nfreq, 2, npix)) * sensitivities[:, None, None] ** 2

    noise = np.random.randn(nfreq, 2, npix) * np.sqrt(covariance)
    data += noise

    templates = (dust_template, sync_template, cmb_template)
    scaled_maps = (dust_scaled, sync_scaled, cmb_scaled)
    return (
        freq_obs,
        request.param[0],
        request.param[1],
        templates,
        scaled_maps,
        data,
        covariance,
    )


def test_max(fake_data):
    """ This test runs the simplest possible component separation case where we know the
    model exactly, and there is no spatial variation in either amplitudes or spectral
    indices.

    The data is generated as a three component model: CMB, dust, synchrotron, all of which have
    spatially uniform emission and SEDs. The test is run with multiple values of the spectral
    parameters.

    The observed data has very low noise (RMS 0.2 in each pixel at each frequency) so the
    model should be very well constrained.

    The data is generated at Nfreq frequencies. Nfreq >~ 10 should result in very good results,
    suitable for testing the code.
    """
    from mesmer import LogProb
    import numpy as np
    from scipy.optimize import minimize
    from jax import grad, jacfwd, jacrev

    (
        frequencies,
        true_beta_s,
        true_beta_d,
        templates,
        scaled_maps,
        data,
        covariance,
    ) = fake_data
    dust_template, sync_template, cmb_template = templates
    dust_scaled, sync_scaled, cmb_scaled = scaled_maps
    true_params = np.array([true_beta_d, true_beta_s])
    model = {
        "dustmbb": {
            "varied": {"beta_d": [1.5, 0.5]},
            "fixed": {"T_d": 20.0, "nu_ref_d": 353.0},
        },
        "syncpl": {"varied": {"beta_s": [-3.0, 0.5]}, "fixed": {"nu_ref_s": 23.0}},
        "cmb": {"varied": {}, "fixed": {}},
    }
    logprob = LogProb(
        data=data, covariance=covariance, frequencies=frequencies, model=model
    )

    dlnP_dTheta = grad(logprob, 0)

    print("Log prob derivative Bd", dlnP_dTheta(true_params, True))
    print(
        "Log prob derivative compared to logprob: ",
        dlnP_dTheta(true_params) / logprob(true_params),
    )

    hessian = jacfwd(jacrev(logprob))
    hessian_eval = hessian(true_params, True)
    print("Hessian evaluated", hessian_eval)

    fish_est = np.linalg.inv(hessian_eval)
    print(
        "Fishers estimates of uncertainty: ",
        np.sqrt(fish_est[0, 0]),
        np.sqrt(fish_est[1, 1]),
    )

    marg_errors = np.sqrt(np.array([fish_est[0, 0], fish_est[1, 1]]))

    res = minimize(
        logprob, [true_beta_d, true_beta_s], tol=1e-9, args=(True), method="Powell"
    )
    dust = logprob.get_amplitude_expectation(res.x, component="dustmbb")
    cmb = logprob.get_amplitude_expectation(res.x, component="cmb")
    sync = logprob.get_amplitude_expectation(res.x, component="syncpl")
    print(f"Dust, input mean {np.mean(dust_template)} recovered mean {np.mean(dust)}")
    print(f"CMB, input_mean {np.mean(cmb_template)} recovered mean {np.mean(cmb)}")
    print(f"Sync, input mean {np.mean(sync_template)} recovered mean {np.mean(sync)}")
    print(f"True parameters {true_params}, recovered parameters {res.x}")
    print(f"Parameter error {(true_params - res.x) / marg_errors}-sigma")

    # Assert that the difference between true parameters and recovered is less than
    # three times the calculated uncertainty.
    np.testing.assert_array_less(true_params - res.x, 5.0 * marg_errors)
    return
