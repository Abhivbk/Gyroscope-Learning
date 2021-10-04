from MPU6050_I2c.MPU6050 import MPU6050

i2c_bus = 1
device_address = 0x68
# The offsets are different for each device and should be changed
# accordingly using a calibration procedure
x_accel_offset = 2606
y_accel_offset = 1211
z_accel_offset = -788
x_gyro_offset = -19
y_gyro_offset = 41
z_gyro_offset = -21

orientation = ""

enable_debug_output = True

mpu = MPU6050(i2c_bus, device_address, x_accel_offset, y_accel_offset,
              z_accel_offset, x_gyro_offset, y_gyro_offset, z_gyro_offset,
              enable_debug_output)

mpu.dmp_initialize()
mpu.set_DMP_enabled(True)
mpu_int_status = mpu.get_int_status()
print(hex(mpu_int_status))

packet_size = mpu.DMP_get_FIFO_packet_size()
print(packet_size)
FIFO_count = mpu.get_FIFO_count()
print(FIFO_count)

FIFO_buffer = [0] * 64

FIFO_count_list = list()


def main():
    while True:
        try:
            FIFO_count = mpu.get_FIFO_count()
            mpu_int_status = mpu.get_int_status()

            # If overflow is detected by status or fifo count we want to reset
            if (FIFO_count == 1024) or (mpu_int_status & 0x10):
                mpu.reset_FIFO()
            #             # Check if fifo data is ready
            elif (mpu_int_status & 0x02):  # Wait until packet_size number of bytes are ready for reading, default
                # is 42 bytes
                while FIFO_count < packet_size:
                    FIFO_count = mpu.get_FIFO_count()
                    FIFO_buffer = mpu.get_FIFO_bytes(packet_size)
                    # accel = mpu.DMP_get_acceleration_int16(FIFO_buffer)
                    quat = mpu.DMP_get_quaternion_int16(FIFO_buffer)
                    grav = mpu.DMP_get_gravity(quat)
                    # acceleration = mpu.get_acceleration()
                    roll_pitch_yaw = mpu.DMP_get_euler_roll_pitch_yaw(quat, grav)

                    roll = str(round(roll_pitch_yaw.x))
                    pitch = round(roll_pitch_yaw.y)
                    yaw = round(roll_pitch_yaw.z)

                    print(f"Yaw:{yaw} Pitch: {pitch} Roll: {roll}")
                    with open('orientation.txt', 'w') as f:
                        f.write(roll)
                    # if roll > 25:
                    #     orientation = 'Moving Right'
                    # elif roll < -25:
                    #     orientation = "Moving Left"
                    #
                    # elif pitch > 25:
                    #     orientation = 'Moving Backward'
                    # elif pitch < -25:
                    #     orientation = 'Moving Forward'
                    #
                    # else:
                    #     orientation = 'Flat on Table'
                    #
                    # print(f"Orientation: {orientation}")

        except ZeroDivisionError:
            pass


if __name__ == '__main__':
    main()

    # end = time.time()
    #
    # u_0 = acceleration[0]
    # u_1 = acceleration[1]
    # u_2 = acceleration[2]
    #
    # a = 9.8
    # t = start - end
    # u = (u_2 - u_1 - u_0)
    # s = 0
    #
    # v = u + a * t
    # s = (v * v) - (u * u) / 2 * a
    #
    # altitude = float( str( s )[0:6] )
    # print(altitude)
    # if count % 100 == 0:
    #     print('roll: ' + str(roll_pitch_yaw.x))
    #     print('pitch: ' + str(roll_pitch_yaw.y))
    #     print('yaw: ' + str(roll_pitch_yaw.z))
    # count += 1
    # except ZeroDivisionError:
    #     pass
