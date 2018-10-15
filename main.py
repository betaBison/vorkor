from visualize3d import visualization




def main():

    graph = visualization("short",12)

    while(1):
        graph.update_graph()

if __name__ == '__main__':
    main()