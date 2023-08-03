import math

class EuclideanDistTracker:
    def __init__(self, dist_limit=25):
        self.center_points = {}
        self.id_count = 0
        self.dist_limit = dist_limit

    def get_centroid(self, rectangle):
        x, y, w, h = rectangle
        cx = (x + x + w) // 2
        cy = (y + y + h) // 2
        return cx, cy

    def calculate_distance(self, c1, c2):
        return math.hypot(c1[0] - c2[0], c1[1] - c2[1])

    def find_existing_object(self, centroid):
        for object_id, center_point in self.center_points.items():
            dist = self.calculate_distance(centroid, center_point)
            if dist < self.dist_limit:
                return object_id
        return None

    def update_existing_object(self, object_id, centroid):
        self.center_points[object_id] = centroid

    def add_new_object(self, centroid):
        self.center_points[self.id_count] = centroid
        new_object_id = self.id_count
        self.id_count += 1
        return new_object_id

    def update(self, objects_rect):
        objects_bbs_ids = []

        for rect in objects_rect:
            centroid = self.get_centroid(rect)
            existing_object_id = self.find_existing_object(centroid)

            if existing_object_id is not None:
                self.update_existing_object(existing_object_id, centroid)
                objects_bbs_ids.append([*rect, existing_object_id])
            else:
                new_object_id = self.add_new_object(centroid)
                objects_bbs_ids.append([*rect, new_object_id])

        self.center_points = {object_id: centroid for object_id, centroid in self.center_points.items() if object_id in {bb_id for _, _, _, _, bb_id in objects_bbs_ids}}

        return objects_bbs_ids


