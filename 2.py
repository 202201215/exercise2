import sqlite3

# 读取文件并将内容复制到列表中
stephen_king_adaptations_list = []
try:
    with open('stephen_king_adaptations.txt', 'r') as file:
        for line in file:
            stephen_king_adaptations_list.append(line.strip())
except FileNotFoundError:
    print("找不到指定的文件 'stephen_king_adaptations.txt'！请确保该文件存在于当前目录中。")
    exit(1)

# 连接到数据库
try:
    connection = sqlite3.connect('stephen_king_adaptations.db')
    cursor = connection.cursor()

    # 创建表
    cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table
                      (movie_id TEXT, movie_name TEXT, movie_year INTEGER, imdb_rating REAL)''')

    # 将内容插入表中
    for movie in stephen_king_adaptations_list:
        movie_data = movie.split(',')
        if len(movie_data) == 4:
            cursor.execute("INSERT INTO stephen_king_adaptations_table VALUES (?,?,?,?)", movie_data)
        else:
            print(f"忽略格式错误的行: {movie}")

    # 提交更改
    connection.commit()

    # 用户交互
    while True:
        print("请选择搜索选项：")
        print("1. 电影名称")
        print("2. 电影年份")
        print("3. 电影评分")
        print("4. 停止")

        option = input("请输入选项数字：")

        if option == '1':
            movie_name = input("请输入要搜索的电影名称：")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movie_name=?", (movie_name,))
            result = cursor.fetchall()

            if result:
                for row in result:
                    print("电影ID:", row[0])
                    print("电影名称:", row[1])
                    print("电影年份:", row[2])
                    print("IMDB评级:", row[3])
            else:
                print("我们的数据库中不存在此类电影。")

        elif option == '2':
            movie_year = input("请输入要搜索的电影年份：")
            try:
                movie_year = int(movie_year)
            except ValueError:
                print("输入的电影年份无效！请确保输入一个整数。")
                continue

            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movie_year=?", (movie_year,))
            result = cursor.fetchall()

            if result:
                for row in result:
                    print("电影ID:", row[0])
                    print("电影名称:", row[1])
                    print("电影年份:", row[2])
                    print("IMDB评级:", row[3])
            else:
                print("未找到在我们的数据库中的那一年的电影。")

        elif option == '3':
            imdb_rating = input("请输入评级限制：")
            try:
                imdb_rating = float(imdb_rating)
            except ValueError:
                print("输入的评级限制无效！请确保输入一个数字。")
                continue

            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdb_rating >= ?", (imdb_rating,))
            result = cursor.fetchall()

            if result:
                for row in result:
                    print("电影ID:", row[0])
                    print("电影名称:", row[1])
                    print("电影年份:", row[2])
                    print("IMDB评级:", row[3])
            else:
                print("没有在数据库中找到达到或超过该评级的电影。")

        elif option == '4':
            break

except sqlite3.Error as e:
    print("在操作数据库时出现错误:", e)
    exit(1)
finally:
    # 关闭连接
    if connection:
        connection.close()