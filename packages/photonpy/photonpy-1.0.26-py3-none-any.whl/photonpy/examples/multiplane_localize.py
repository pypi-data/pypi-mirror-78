# -*- coding: utf-8 -*-


############################## Gaussian 3D #####################################

def run_frame(inp):
    frame, positions, z = inp
    roi_size = 14  # TODO: Turn into input

    sigmas = []
    rois = get_rois(frame, positions, roi_size=roi_size)
    for roi in rois:
        r = fit_sigma_3d(roi)
        if min(r[:2]) > 2 and max(r[:2]) < (roi_size - 2):
            sigmas.append((z, r[Params3D.SIGMA_X], r[Params3D.SIGMA_Y]))

    return sigmas


def calibrate_gaussian_3D(movie, output, args):
    z_range = np.linspace(-args.zrange * 1e-3, args.zrange * 1e-3, num=len(movie))
    in_focus = movie[int(len(movie) / 2)]

    positions = get_peak_positions(in_focus)
    inputs = []

    # shifts = []
    # with SMLM(debugMode=False) as smlm, Context(smlm) as ctx:
    #     gaussian = Gaussian(ctx)
    #     psf = gaussian.CreatePSF_XYIBgSigmaXY(roisize, (2, 2), False)

    #     for p in psfs:
    #         theta, _, tr = psf.ComputeMLE(1e5 * p)
    #         ss = theta[:, -2] + theta[:, -1]
    #         ss[theta[:, 0] < 3] = np.inf
    #         ss[theta[:, 0] > roisize - 2] = np.inf
    #         ss[theta[:, 1] < 3] = np.inf
    #         ss[theta[:, 1] > roisize - 2] = np.inf

    #         ii = np.argmin(ss)
    #         t = theta[ii]
    #         shifts.append([t[0] - (roisize / 2 - 0.5),
    #                        t[1] - (roisize / 2 - 0.5),
    #                        ii - len(p) / 2])

    for i, z in enumerate(z_range):
        inputs.append((movie[i], positions, z))

    with Pool() as p:
        results = p.map(run_frame, inputs)

    zs = []
    sigma_xs = []
    sigma_ys = []
    for r in results:
        for z, sigma_x, sigma_y in r:
            zs.append(z)
            sigma_xs.append(sigma_x)
            sigma_ys.append(sigma_y)

    def f(p, z):
        s0, gamma, d, A = p
        return s0 * np.sqrt(1 + (z - gamma) ** 2 / d ** 2 + A * (z - gamma) ** 3 / d ** 2)

    def func(p, z, y):
        return f(p, z) - y

    bounds = ((0.1, -600, 0, 1e-6), (10, 600, 1e3, 1e-1))
    p0 = [2, 0, 3e2, 1e-5]
    p_x = least_squares(func, p0, loss="huber", bounds=bounds, args=(zs, sigma_xs))
    p_y = least_squares(func, p0, loss="huber", bounds=bounds, args=(zs, sigma_ys))

    calibration = {"x": p_x.x, "y": p_y.x}

    print(positions)
    print(calibration)
    np.save(output, calibration)

    # plt.plot(zs, sigma_xs, 'x', label='\sigma_x')
    # plt.plot(zs, sigma_ys, 'x', label='\sigma_y')
    # plt.plot(zs, f(p_x.x, zs), '--', label='x fit')
    # plt.plot(zs, f(p_y.x, zs), '--', label='y fit')
    # plt.ylim([0, max(np.max(sigma_xs), np.max(sigma_ys))])
    # plt.legend()
    # plt.show()