import unittest
import zeef_van_eratosthenes as zeef


class MyTestCase(unittest.TestCase):

    def test_primes(self):
        validated_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89,
                            97,
                            101, 103, 107, 109]
        prime_list = zeef.zeef(120)
        for index, prime in enumerate(validated_primes):
            self.assertEqual(prime, prime_list[index])

if __name__ == '__main__':
    unittest.main()
