bl_info = {
    "name": "Weight Averaging",
    "author": "Inwerwm",
    "version": (1, 0),
    "blender": (3, 3, 1),
    "location": "",
    "description": "Averages the weights of the selected vertices.",
    "warning": "",
    "support": "TESTING",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}


def register():
    print("Enable Weight Averaging")


def unregister():
    print("Disable Weight Averaging")


if __name__ == "__main__":
    register()
