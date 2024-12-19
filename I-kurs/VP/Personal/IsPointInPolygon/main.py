import json
import matplotlib.pyplot as plt


def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def is_inside(edges, xp, yp):
    cnt = 0
    for edge in edges:
        (x1, y1), (x2, y2) = edge

        if (yp < y1) != (yp < y2) and (xp < x1 + ((yp-y1) / (y2-y1))*(x2-x1)):
            cnt += 1

    return cnt % 2 == 1


def onclick(event):
    xp, yp = event.xdata, event.ydata

    kvname = "Outside"

    plt.plot(xp, yp, 'go', markersize=10)
    plt.gcf().canvas.draw()

    for kv in data['features']:
        geometry = kv['geometry']
        if geometry['type'] != 'MultiPolygon':
            continue

        points = geometry['coordinates'][0][0]
        edges = list(zip(points, points[1:] + [points[0]]))

        if is_inside(edges, xp, yp):
            kvname = kv['properties']['kvname']
            break

    print(kvname)


if __name__ == "__main__":
    file_path = 'data.json'
    data = load_data(file_path)

    plt.figure(figsize=(10, 10))
    plt.gca().set_aspect('equal')

    for kv in data['features']:
        geometry = kv['geometry']
        if geometry['type'] != 'MultiPolygon':
            continue

        points = geometry['coordinates'][0][0]
        edges = list(zip(points, points[1:] + [points[0]]))

        xs, ys = zip(*points)

        plt.plot(xs, ys)

    plt.gcf().canvas.mpl_connect('button_press_event', onclick)

    plt.show()
