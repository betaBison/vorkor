from visualize3d import visualization


def main():
    # visualization("short" or "long", number of intruders,
    #                   "body" or "static" inertial frame)
    graph = visualization("long",20,"body")

    while(True):
        graph.update_graph()

if __name__ == '__main__':
    main()