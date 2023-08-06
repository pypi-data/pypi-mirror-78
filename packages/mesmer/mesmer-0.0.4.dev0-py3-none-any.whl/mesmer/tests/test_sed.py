def test_fmatrix():
    import numpy as np
    from mesmer.seds import FMatrix

    freqs = np.logspace(1, 3, 100)
    components = ["cmb", "syncpl", "dustmbb"]
    fmatrix = FMatrix(components)

    parameters = {
        "nu": freqs,
        "nu_ref_d": 353.0,
        "nu_ref_s": 23.0,
        "beta_d": 1.5,
        "beta_s": -3.0,
        "T_d": 20.0,
    }

    output1 = fmatrix(**parameters)
    assert output1.shape == (len(components), len(freqs))

    parameters.pop("nu")
    # Check that the same answer is achieved by calling FMatrix
    # in a different way.
    output2 = fmatrix(nu=freqs, **parameters)
    np.testing.assert_array_equal(output1, output2)
    return


def test_dustmbb():
    from mesmer.seds import dustmbb
    from jax import grad
    import numpy as np

    nu = 100.0
    nu_ref_d = 353.0
    beta_d = 1.5
    T_d = 20.0

    # compare analytic gradient to jax gradient
    df_db = grad(dustmbb, argnums=2)
    df_db_0 = df_db(nu, nu_ref_d, beta_d, T_d)
    df_db_1 = dustmbb(nu, nu_ref_d, beta_d, T_d) * np.log(nu / nu_ref_d)
    np.testing.assert_almost_equal(df_db_0, df_db_1)


def test_syncpl():
    from mesmer.seds import syncpl
    from jax import grad
    import numpy as np

    nu = 100.0
    nu_ref_s = 23.0
    beta_s = -3.0

    # compare analytic gradient to jax gradient
    df_db = grad(syncpl, 2)
    df_db_0 = df_db(nu, nu_ref_s, beta_s)
    df_db_1 = (nu / nu_ref_s) ** beta_s * np.log(nu / nu_ref_s)
    np.testing.assert_almost_equal(df_db_0, df_db_1)
