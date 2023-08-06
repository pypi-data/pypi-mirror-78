import unittest
import os


class TestBase(unittest.TestCase):
    def get_file_path(self, fic):
        pth = os.path.join(os.path.dirname(__file__), fic)
        return pth

    def write_data_file(self, dat, fic):
        pth = self.get_fic_path(fic)
        f = open(pth, "w")

        ns = len(dat)
        for i in range(ns):
            f.write("%f, %f\n" % (np.real(dat[i]), np.imag(dat[i])))

        f.close()

    def read_data_file(self, fic):
        pth = self.get_file_path(fic)
        f = open(pth, "r")
        l = f.readlines()
        f.close()

        ns = len(l)
        ref = np.empty(ns, dtype=np.complex64)
        for i in range(ns):
            r = l[i]
            x, y = [float(v.strip()) for v in r.strip().split(",")]
            ref[i] = x + y * 1j

        return ref

    def compare_data_ref(self, dat, fic_ref):
        ref = self.read_data_file(fic_ref)
        err = np.max(np.abs(dat - ref))
        return err
