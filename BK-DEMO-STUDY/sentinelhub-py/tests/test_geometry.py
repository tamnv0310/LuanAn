import unittest
import copy

import shapely.geometry

from sentinelhub import BBox, Geometry, BBoxCollection, CRS, get_utm_crs, TestSentinelHub


class TestBBox(TestSentinelHub):
    def test_bbox_no_crs(self):
        with self.assertRaises(TypeError):
            BBox('46,13,47,20')

    def test_bbox_from_string(self):
        bbox_str = '46.07, 13.23, 46.24, 13.57'
        bbox = BBox(bbox_str, CRS.WGS84)
        self.assertEqual(bbox.lower_left, (46.07, 13.23))
        self.assertEqual(bbox.upper_right, (46.24, 13.57))
        self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_bad_string(self):
        with self.subTest(msg="Too few coordinates"):
            bbox_str = '46.07, 13.23, 46.24'
            with self.assertRaises(ValueError):
                BBox(bbox_str, CRS.WGS84)

        with self.subTest(msg="Invalid string"):
            bbox_str = '46N,13E,45N,12E'
            with self.assertRaises(ValueError):
                BBox(bbox_str, CRS.WGS84)

    def test_bbox_from_flat_list(self):
        for bbox_lst in [[46.07, 13.23, 46.24, 13.57], [46.24, 13.23, 46.07, 13.57],
                         [46.07, 13.57, 46.24, 13.23], [46.24, 13.57, 46.07, 13.23]]:
            with self.subTest(msg="bbox={}".format(bbox_lst)):
                bbox = BBox(bbox_lst, CRS.WGS84)
                self.assertEqual(bbox.lower_left, (46.07, 13.23))
                self.assertEqual(bbox.upper_right, (46.24, 13.57))
                self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_nested_list(self):
        bbox_lst = [[-46.07, -13.23], [46.24, 13.57]]
        bbox = BBox(bbox_lst, CRS.WGS84)
        self.assertEqual(bbox.upper_right, (46.24, 13.57))
        self.assertEqual(bbox.lower_left, (-46.07, -13.23))
        self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_flat_tuple(self):
        bbox_tup = 46.07, 13.23, 46.24, 13.57
        bbox = BBox(bbox_tup, CRS.WGS84)
        self.assertEqual(bbox.upper_right, (46.24, 13.57))
        self.assertEqual(bbox.lower_left, (46.07, 13.23))
        self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_nested_tuple(self):
        bbox_tup = (46.07, 13.23), (46.24, 13.57)
        bbox = BBox(bbox_tup, CRS.WGS84)
        self.assertEqual(bbox.upper_right, (46.24, 13.57))
        self.assertEqual(bbox.lower_left, (46.07, 13.23))
        self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_list_tuple_combo(self):
        bbox_list = [(46.07, 13.23), (46.24, 13.57)]
        bbox = BBox(bbox_list, CRS.WGS84)
        self.assertEqual(bbox.upper_right, (46.24, 13.57))
        self.assertEqual(bbox.lower_left, (46.07, 13.23))
        self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_dict(self):
        bbox_dict = {'min_x': 46.07, 'min_y': 13.23, 'max_x': 46.24, 'max_y': 13.57}
        bbox = BBox(bbox_dict, CRS.WGS84)
        self.assertEqual(bbox.upper_right, (46.24, 13.57))
        self.assertEqual(bbox.lower_left, (46.07, 13.23))
        self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_bad_dict(self):
        bbox_dict = {'x1': 46.07, 'y1': 13.23, 'x2': 46.24, 'y2': 13.57}
        with self.assertRaises(KeyError):
            BBox(bbox_dict, CRS.WGS84)

    def test_bbox_from_bbox(self):
        bbox_dict = {'min_x': 46.07, 'min_y': 13.23, 'max_x': 46.24, 'max_y': 13.57}
        bbox_fst = BBox(bbox_dict, CRS.WGS84)
        bbox = BBox(bbox_fst, CRS.WGS84)

        self.assertEqual(bbox.upper_right, (46.24, 13.57))
        self.assertEqual(bbox.lower_left, (46.07, 13.23))
        self.assertEqual(bbox.crs, CRS.WGS84)

    def test_bbox_from_shapely(self):
        bbox_list = [
            BBox(shapely.geometry.LineString([(0, 0), (1, 1)]), CRS.WGS84),
            BBox(shapely.geometry.LinearRing([(1, 0), (1, 1), (0, 0)]), CRS.WGS84),
            BBox(shapely.geometry.Polygon([(1, 0), (1, 1), (0, 0)]), CRS.WGS84)
        ]
        for bbox in bbox_list:
            self.assertEqual(bbox, BBox((0, 0, 1, 1), CRS.WGS84))

    def test_bbox_to_str(self):
        x1, y1, x2, y2 = 45.0, 12.0, 47.0, 14.0
        crs = CRS.WGS84
        expect_str = "{},{},{},{}".format(x1, y1, x2, y2)
        bbox = BBox(((x1, y1), (x2, y2)), crs)
        self.assertEqual(str(bbox), expect_str,
                         msg="String representations not matching: expected {}, got {}".format(expect_str, str(bbox)))

    def test_bbox_to_repr(self):
        x1, y1, x2, y2 = 45.0, 12.0, 47.0, 14.0
        bbox = BBox(((x1, y1), (x2, y2)), crs=CRS('4326'))
        expect_repr = "BBox((({}, {}), ({}, {})), crs=CRS('4326'))".format(x1, y1, x2, y2)
        self.assertEqual(repr(bbox), expect_repr,
                         msg="String representations not matching: expected {}, got {}".format(expect_repr, repr(bbox)))

    def test_bbox_iter(self):
        bbox_lst = [46.07, 13.23, 46.24, 13.57]
        bbox = BBox(bbox_lst, CRS.WGS84)
        bbox_iter = [coord for coord in bbox]
        self.assertEqual(bbox_iter, bbox_lst,
                         msg="Expected {}, got {}".format(bbox_lst, bbox_iter))

    def test_bbox_eq(self):
        bbox1 = BBox([46.07, 13.23, 46.24, 13.57], CRS.WGS84)
        bbox2 = BBox(((46.24, 13.57), (46.07, 13.23)), 4326)
        bbox3 = BBox([46.07, 13.23, 46.24, 13.57], CRS.POP_WEB)
        bbox4 = BBox([46.07, 13.23, 46.24, 13.58], CRS.WGS84)
        self.assertEqual(bbox1, bbox2, "Bounding boxes {} and {} should be the same".format(repr(bbox1), repr(bbox2)))
        self.assertNotEqual(bbox1, bbox3, "Bounding boxes {} and {} should not be the same".format(repr(bbox1),
                                                                                                   repr(bbox3)))
        self.assertNotEqual(bbox1, bbox4, "Bounding boxes {} and {} should not be the same".format(repr(bbox1),
                                                                                                   repr(bbox4)))
        self.assertNotEqual(bbox1, None)

    def test_transform(self):
        bbox1 = BBox([46.07, 13.23, 46.24, 13.57], CRS.WGS84)
        bbox2 = bbox1.transform(CRS.POP_WEB).transform(CRS.WGS84)

        for coord1, coord2 in zip(bbox1, bbox2):
            self.assertAlmostEqual(coord1, coord2, delta=1e-8)
        self.assertEqual(bbox1.crs, bbox2.crs)

    def test_transform_bounds(self):
        bbox1 = BBox([46.07, 13.23, 46.24, 13.57], CRS.WGS84)
        utm_crs = get_utm_crs(*bbox1.middle, CRS.WGS84)
        bbox2 = bbox1.transform_bounds(utm_crs).transform_bounds(CRS.WGS84)

        self.assertTrue(bbox2.geometry.contains(bbox1.geometry))
        self.assertGreater(bbox2.geometry.difference(bbox1.geometry).area, 1e-4)

    def test_geometry(self):
        bbox = BBox([46.07, 13.23, 46.24, 13.57], CRS.WGS84)

        self.assertTrue(isinstance(bbox.get_geojson(), dict),
                        "Expected dictionary, got type {}".format(type(bbox.geometry)))
        self.assertTrue(isinstance(bbox.geometry, shapely.geometry.Polygon),
                        "Expected type {}, got type {}".format(shapely.geometry.Polygon,
                                                               type(bbox.geometry)))

    def test_buffer(self):
        bbox = BBox([46.07, 13.23, 46.24, 13.57], CRS.WGS84)

        self.assertEqual(bbox, bbox.buffer(0), "Buffer 1 should not change bounding box")
        self.assertEqual(bbox, bbox.buffer(1).buffer(-0.5), "Twice buffered bounding box should return to original")


class TestGeometry(TestSentinelHub):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        polygon = shapely.geometry.Polygon([(465888.8773268595, 5079639.43613863),
                                            (465885.3413983975, 5079641.52461826),
                                            (465882.9542217017, 5079647.16604353),
                                            (465888.8780175466, 5079668.70367663),
                                            (465888.877326859, 5079639.436138632)])
        cls.wkt_string = 'MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)), ((20 35, 10 30, 10 10, 30 5, 45 20, 20 35), ' \
                         '(30 20, 20 15, 20 25, 30 20)))'
        cls.geometry1 = Geometry(polygon, CRS(32633))
        cls.geometry2 = Geometry(cls.wkt_string, CRS.WGS84)
        cls.bbox = BBox(bbox=[14.00, 45.00, 14.03, 45.03], crs=CRS.WGS84)
        cls.bbox_collection = BBoxCollection([cls.bbox, BBox('46,13,47,20', CRS.WGS84)])

        cls.geometry_list = [cls.geometry1, cls.geometry2, cls.bbox, cls.bbox_collection]

    def test_repr(self):
        for geometry in self.geometry_list:
            self.assertTrue(isinstance(repr(geometry), str), 'Expected string representation')

    def test_eq(self):
        for geometry in self.geometry_list:
            self.assertEqual(geometry, copy.deepcopy(geometry), 'Deep copied object should be the same as original')
            self.assertNotEqual(geometry, None)

    def test_reverse(self):
        for geometry in self.geometry_list:
            reversed_geometry = geometry.reverse()
            self.assertNotEqual(geometry, reversed_geometry, 'Reversed geometry should be different')
            self.assertEqual(geometry, reversed_geometry.reverse(), 'Twice reversed geometry should equal the original')

    def test_transform(self):
        for geometry in self.geometry_list:
            new_geometry = geometry.transform(CRS.POP_WEB)
            self.assertNotEqual(geometry, new_geometry, 'Transformed geometry should be different')

            original_geometry = geometry.transform(geometry.crs)
            self.assertEqual(geometry.crs, original_geometry.crs, 'CRS of twice transformed geometry should preserve')
            self.assertAlmostEqual(geometry.geometry.area, original_geometry.geometry.area, delta=1e-10,
                                   msg='Geometry area should be equal')

    def test_geojson(self):
        for geometry in [self.geometry1, self.geometry2]:
            self.assertEqual(geometry, Geometry(geometry.geojson, geometry.crs),
                             'Transforming geometry to geojson and back should preserve it')

    def test_wkt(self):
        for geometry in [self.geometry1, self.geometry2]:
            self.assertEqual(geometry, Geometry(geometry.wkt, geometry.crs),
                             'Transforming geometry to geojson and back should preserve it')

        self.assertEqual(self.geometry2.wkt, self.wkt_string, 'New WKT string does not match the original')

    def test_bbox(self):
        for geometry in [self.geometry1, self.geometry2, self.bbox_collection]:
            self.assertEqual(geometry.bbox, BBox(geometry.geometry, geometry.crs), 'Failed bbox property')


if __name__ == '__main__':
    unittest.main()
