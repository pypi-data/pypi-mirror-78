test file=gif2char.py code
    #!/usr/bin/python
    import argparse
    from modul.gif2txt import gif2txt
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-d','--duration',type = float, default = 1)#播放时间
    #获取参数
    args = parser.parse_args()
    File = args.file
    DURARION = args.duration

    cls=gif2txt.gif2txt(file=File,duration=DURARION,debug=True)
    cls.make() #生成gif



[root@localhost code]# python gif2char.py timg_2.gif -d 0.1