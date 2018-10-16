from visualize3d import visualization


def main():
    # visualization("short" or "long", # intruders)
    graph = visualization("short",12)

    while(1):
        graph.update_graph()

if __name__ == '__main__':
    main()