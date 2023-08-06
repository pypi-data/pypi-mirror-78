from typing import List

import numpy as np
import pandas as pd
import geopandas as gpd

from unittest import TestCase
from multiprocessing import Pool

from pyproj import CRS

from transpy import split_linestring, split_linestring_df
from shapely.geometry import LineString, Point, MultiLineString

from transpy.utils import to_chunk


class TestSplitLineString(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._geometry_samples = [
            {
                'geometry': LineString([(0, 0), (10, 0), (10, 5)]),
                'length': 15
            },
            {
                'geometry': LineString([(0, 0), (-10, 0), (-10, -5)]),
                'length': 15
            }
        ]

        cls._pool = Pool(processes=2)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._pool.close()

    @staticmethod
    def get_sample_LineString_list(
            max_length: int = 2,
            n_geometry: int = 4) -> List[LineString]:
        x = list(range(max_length, (n_geometry+1) * max_length, max_length))
        ls_iterator = [
            LineString([(0, 0), (e, 0)])
            for e in x
        ]
        return ls_iterator

    @staticmethod
    def get_sample_LineString_gdf_epsg_3857(
            max_length: int = 2,
            n_geometry: int = 4) -> gpd.GeoDataFrame:
        ls_iterator = TestSplitLineString.get_sample_LineString_list(max_length, n_geometry)
        gdf = gpd.GeoDataFrame(
            data={
                'id': list(range(n_geometry)),
                'orig_length': list(map(lambda e: e.length, ls_iterator))
            },
            geometry=ls_iterator
        )

        gdf.crs = 'EPSG:3857'
        return gdf

    def test_split_linestring_01(self):
        ls = self._geometry_samples[0]['geometry']
        expected_length = self._geometry_samples[0]['length']
        self.assertEqual(expected_length, ls.length)

        max_length = np.random.randint(1, ls.length)
        split_ls = split_linestring(geometry=ls, max_length=max_length)

        for e in split_ls:
            if (np.abs(e.length - max_length) >= 0.00001):
                print('dsfsdf', e.length,max_length, np.abs(e.length - max_length))
            self.assertTrue(
                (np.abs(e.length - max_length) < 0.00001) or
                e.length <= max_length
            )

    def test_split_linestring_02(self):
        ls = self._geometry_samples[0]['geometry']
        length = self._geometry_samples[0]['length']

        max_length = length+1
        split_ls = split_linestring(geometry=ls, max_length=max_length)

        self.assertEqual(1, len(split_ls))

        for e in split_ls:
            self.assertTrue(e.length <= max_length)

    def test_split_linestring_03(self):
        split_ls = split_linestring(
            geometry=Point(0, 0),
            max_length=42
        )

        self.assertEqual(1, len(split_ls))
        self.assertEqual(Point(0, 0), split_ls[0])

    def test_split_linestring_04(self):
        mls = MultiLineString([
            self._geometry_samples[0]['geometry'],
            self._geometry_samples[1]['geometry']
        ])
        expected_length = self._geometry_samples[0]['length'] + self._geometry_samples[1]['length']

        self.assertEqual(expected_length, mls.length)

        max_length = np.random.randint(1, mls.length)
        split_mls = split_linestring(mls, max_length)
        for e in split_mls:
            self.assertTrue(e.length <= max_length)

    def test_split_linestring_05(self):
        max_length = 2
        n_geometry = 4
        ls_iterator = TestSplitLineString.get_sample_LineString_list(max_length, n_geometry)


        results = split_linestring(ls_iterator, max_length)
        self.assertEqual(n_geometry, len(results))
        for i in range(n_geometry):
            self.assertEqual(i + 1, len(results[i]))
            for e in results[i]:
                self.assertAlmostEqual(e.length, max_length, places=2)

    def test_split_linestring_06(self):
        max_length = 2
        n_geometry = 500
        ls_iterator = TestSplitLineString.get_sample_LineString_list(max_length, n_geometry)

        results = split_linestring(ls_iterator, max_length, self._pool)
        self.assertEqual(n_geometry, len(results))
        for i in range(n_geometry):
            self.assertEqual(i + 1, len(results[i]))
            for e in results[i]:
                self.assertAlmostEqual(e.length, max_length, places=2)

    def test_split_linestring_df_01(self):
        max_length = 2
        n_geometry = 4
        gdf = TestSplitLineString.get_sample_LineString_gdf_epsg_3857(max_length, n_geometry)

        # print(gdf)

        split_gdf = split_linestring_df(
            df=gdf,
            max_length=max_length,
        )

        # print(split_gdf)
        expected_n_rows = np.sum(np.arange(1, n_geometry + 1))
        self.assertEqual(expected_n_rows, split_gdf.shape[0])
        for e in split_gdf.geometry:
            self.assertAlmostEqual(e.length, max_length, places=2)

    def test_split_linestring_df_02(self):
        max_length = 2
        n_geometry = 500
        gdf = TestSplitLineString.get_sample_LineString_gdf_epsg_3857(max_length, n_geometry)

        # print(gdf)
        split_gdf = split_linestring_df(
            df=gdf,
            max_length=max_length,
            pool=self._pool
        )

        # print(split_gdf)
        expected_n_rows = np.sum(np.arange(1, n_geometry + 1))
        self.assertEqual(expected_n_rows, split_gdf.shape[0])
        for e in split_gdf.geometry:
            self.assertAlmostEqual(e.length, max_length, places=2)

    def test_split_linestring_df_03(self):
        max_length = 2
        n_geometry = 4
        gdf = TestSplitLineString.get_sample_LineString_gdf_epsg_3857(max_length, n_geometry)

        back_up_crs = gdf.crs
        gdf = gdf.to_crs(epsg=4326)

        print(gdf)

        split_gdf = split_linestring_df(
            df=gdf,
            max_length=max_length,
        )

        self.assertEqual(split_gdf.crs, CRS(4326))
        split_gdf = split_gdf.to_crs(epsg=3857)

        expected_n_rows = np.sum(np.arange(1, n_geometry + 1))
        self.assertEqual(expected_n_rows, split_gdf.shape[0])
        for e in split_gdf.geometry:
            self.assertAlmostEqual(e.length, max_length, places=2)

class TestToChunl(TestCase):
    def test_to_chunk_01(self):
        a = [1, 2, 3, 4, 5, 6]
        a_chunk = to_chunk(a, chunk_size=3)

        self.assertEqual(2, len(a_chunk))
        self.assertEqual([1, 2, 3], a_chunk[0])
        self.assertEqual([4, 5, 6], a_chunk[1])

    def test_to_chunk_02(self):
        a = [1, 2, 3, 4, 5, 6]
        a_chunk = to_chunk(a, chunk_size=4)

        self.assertEqual(2, len(a_chunk))
        self.assertEqual([1, 2, 3, 4], a_chunk[0])
        self.assertEqual([5, 6], a_chunk[1])

    def test_to_chunk_03(self):
        a = [1, 2, 3, 4, 5, 6]
        a_chunk = to_chunk(a, n_chunk=2)

        self.assertEqual(2, len(a_chunk))
        self.assertEqual([1, 2, 3], a_chunk[0])
        self.assertEqual([4, 5, 6], a_chunk[1])

    def test_to_chunk_04(self):
        a = [1, 2, 3, 4, 5, 6]
        pool = Pool(processes=2)
        a_chunk = to_chunk(a, pool=pool)

        self.assertEqual(2, len(a_chunk))
        self.assertEqual([1, 2, 3], a_chunk[0])
        self.assertEqual([4, 5, 6], a_chunk[1])

        pool.close()

    def test_to_chunk_05(self):
        a = [1, 2, 3, 4, 5, 6]
        with self.assertRaises(ValueError):
            to_chunk(a, chunk_size=-1)
