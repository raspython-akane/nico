def crow_servo_control(status):
    """
    クローのサーボモーターを制御する
    @param status:サーボモーターのPWMの変化量
    """
    global crow_servo

    # サーボのPWM制御に渡す値を変更する
    # クロー部のサーボの変化量は10倍させる
    crow_servo += status * 10

    # 最大値と最小値を超えた場合はそれぞれの値に戻す
    if crow_servo < crow_min:
        crow_servo = crow_min
    elif crow_servo > crow_max:
        crow_servo = crow_max

    print("クローサーボのPWM制御用の値 : {}".format(crow_servo))

    # サーボの制御モジュールに値を渡す
    # 値は左から(channel, 0, pulse)
    pwm.set_pwm(0, 0, crow_servo)


def arm_left_servo_control(status):
    """
    アーム角度調整用の左側サーボを制御する
    @param status:サーボモーターのPWMの変化量
    """
    global arm_left_servo
    # サーボのPWM制御に渡す値を変更する
    arm_left_servo += status * 10

    # 最大値と最小値を超えた場合はそれぞれの値に戻す
    if arm_left_servo < arm_left_min:
        arm_left_servo = arm_left_min
    elif arm_left_servo > arm_left_max:
        arm_left_servo = arm_left_max

    print("アーム左側サーボのPWM制御用の値 : {}".format(arm_left_servo))

    # サーボの制御モジュールに値を渡す
    # 値は左から(channel, 0, pulse)
    pwm.set_pwm(1, 0, arm_left_servo)


def arm_right_servo_control(status):
    """
    アーム角度調整用の右側サーボを制御する
    @param status:サーボモーターのPWMの変化量
    """
    global arm_right_servo


def base_servo_control(status):
    """
    土台の角度調整用のサーボを制御する
    @param status:サーボモーターのPWMの変化量
    """
    global base_servo
