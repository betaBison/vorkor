from visualize3d import visualization


def main():
    # visualization("short" or "long", # intruders)
    graph = visualization("short",20)

    while(True):
        graph.update_graph()

if __name__ == '__main__':
    main()