import json

class Florence2toCoordinatesButxy:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "data": ("JSON",),
                "source": ("IMAGE",),
                "index": ("STRING", {"default": "0"}),
                "batch": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "BBOX")
    RETURN_NAMES = ("x", "y", "bboxes")
    FUNCTION = "segment"
    CATEGORY = "RinaRalte"

    def segment(self, data, source, index, batch=False):
        # Parse JSON if needed
        if isinstance(data, str):
            try:
                coordinates = json.loads(data.replace("'", "\""))
            except Exception as e:
                print("JSON parsing failed:", e)
                return 0, 0, []
        else:
            coordinates = data

        # Defensive: check structure
        if not (isinstance(coordinates, list) and len(coordinates) > 0 and isinstance(coordinates[0], dict)):
            print("Unexpected data structure:", coordinates)
            return 0, 0, []

        # Index parsing
        if index and index.strip():
            try:
                indexes = [int(i) for i in index.split(",") if i.strip().isdigit()]
            except Exception as e:
                print("Index parsing failed:", e)
                return 0, 0, []
        else:
            # Use all available bboxes
            indexes = list(range(len(coordinates[0].get("bboxes", []))))

        print("bboxes:", coordinates[0].get("bboxes"))
        print("indexes:", indexes)

        top_left_x_points = []
        top_left_y_points = []
        bboxes = []

        bboxes_list = coordinates[0].get("bboxes", [])

        if batch:
            for idx in indexes:
                if 0 <= idx < len(bboxes_list):
                    bbox = bboxes_list[idx]
                    min_x, min_y, max_x, max_y = bbox
                    top_left_x_points.append(int(min_x))
                    top_left_y_points.append(int(min_y))
                    bboxes.append(bbox)
        else:
            for idx in indexes:
                if 0 <= idx < len(bboxes_list):
                    bbox = bboxes_list[idx]
                    min_x, min_y, max_x, max_y = bbox
                    top_left_x_points.append(int(min_x))
                    top_left_y_points.append(int(min_y))
                    bboxes.append(bbox)

        if top_left_x_points and top_left_y_points:
            x_coordinate = top_left_x_points[0]
            y_coordinate = top_left_y_points[0]
        else:
            x_coordinate = 0
            y_coordinate = 0

        print("OUTPUT x:", x_coordinate, "y:", y_coordinate, "bboxes:", bboxes)
        return x_coordinate, y_coordinate, bboxes