def get_greetings(name):
    return "Hello, {0}".format(name)

if __name__ == '__main__': # python my_util.p로 실행한 경우
    message = get_greetings('장동건') 
    print(message)