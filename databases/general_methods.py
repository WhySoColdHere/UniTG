# Используется для стандартного выполнения переданной команды
def cur_exe(command, connect):
    with connect as con:
        cur = con.cursor()
        cur.execute(command)


# Используется для возвращения результата выполнения переданной команды
def cur_exe_return(command, connect):
    with connect as con:
        cur = con.cursor()
        return cur.execute(command)
