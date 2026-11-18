# One cue = one sentence group. en/zh are the narration (spelled for the speech engine); en_sub/zh_sub are what is shown.
CUES = [
 dict(scene=1, en="This is the Meridian I P one irrigation pump. This short video is about one solder joint on its main controller board.",
      en_sub="This is the Meridian IP-1 irrigation pump. This short video is about one solder joint on its main controller board.",
      zh="这是一台手术灌注泵。本视频说明它的主控板上一个焊点的问题。", zh_sub="这是 Meridian IP-1 手术灌注泵。本视频说明它的主控板上一个焊点的问题。"),
 dict(scene=2, en="Inside the pump, the main controller board drives the motor, the valve and the sensors.",
      zh="泵的内部有一块主控板，负责驱动电机、阀门和传感器。"),
 dict(scene=2, en="The problem is at connector J one, the twenty-four volt power input. Pin two is the ground pin.",
      en_sub="The problem is at connector J1, the 24 V power input. Pin 2 is the ground pin.",
      zh="问题出在二十四伏电源输入连接器上，它的第二脚是接地引脚。", zh_sub="问题出在 J1（24 V 电源输入连接器）：第 2 脚是接地引脚。"),
 dict(scene=3, en="This is a cut through that hole. The board has four copper layers, and this pin is tied solidly to the ground copper on three of them.",
      zh="这是这个通孔的剖面。电路板有四层铜，这个引脚与其中三层的接地铜箔是整片直接相连的。"),
 dict(scene=3, en="In wave soldering, solder enters from the bottom. But the large copper areas pull heat out of the hole.",
      zh="波峰焊时，焊锡从底面进入通孔。但是大面积的铜箔把孔里的热量吸走了。"),
 dict(scene=3, en="The solder cools and freezes before it reaches the top. Here it fills only about forty percent of the hole.",
      en_sub="The solder cools and freezes before it reaches the top. Here it fills only about 40% of the hole.",
      zh="焊锡还没有爬到顶面，就冷却凝固了。这里的透锡率只有大约百分之四十。", zh_sub="焊锡还没有爬到顶面，就冷却凝固了。这里的透锡率只有约 40%。"),
 dict(scene=4, en="The requirement for this product is I P C class three. Solder must fill at least seventy-five percent of the hole.",
      en_sub="The requirement for this product is IPC Class 3. Solder must fill at least 75% of the hole.",
      zh="本产品按三级标准验收，通孔透锡率必须达到百分之七十五以上。", zh_sub="本产品按 IPC-A-610 3 级验收，通孔透锡率必须 ≥ 75%。"),
 dict(scene=4, en="From the bottom, this joint looks normal, and the connector body hides the top. A visual check will not catch it.",
      zh="从底面看，这个焊点是正常的，而顶面被连接器本体挡住了，所以目检发现不了这个问题。"),
 dict(scene=4, en="But the joint is weak. With vibration and heat it can crack, and the pump loses power.",
      zh="但是这样的焊点强度不够。在振动和发热的作用下，它可能开裂，导致泵断电。"),
 dict(scene=5, en="Here is what we need changed in the wave soldering process. One: more preheat. The top side of the board at this connector should reach at least one hundred ten degrees Celsius before it touches the wave.",
      en_sub="Here is what we need changed in the wave soldering process. 1: More preheat. The top side of the board at this connector should reach at least 110 °C before it touches the wave.",
      zh="下面是波峰焊工艺需要调整的地方。第一，加强预热。在接触锡波之前，这个连接器位置的板子顶面温度，要达到一百一十摄氏度以上。",
      zh_sub="下面是波峰焊工艺需要调整的地方。第一，加强预热：接触锡波之前，此连接器位置的板子顶面温度要 ≥ 110 °C。"),
 dict(scene=5, en="Two: longer contact time. Slow the conveyor so this pin stays in the solder longer.",
      en_sub="2: Longer contact time. Slow the conveyor so this pin stays in the solder longer.",
      zh="第二，延长接触时间。降低链速，让这个引脚在锡波中停留更久。", zh_sub="第二，延长接触时间：降低链速，让这个引脚在锡波中停留更久。"),
 dict(scene=5, en="Three: flux. Make sure flux gets all the way through the hole to the top side.",
      en_sub="3: Flux. Make sure flux gets all the way through the hole to the top side.",
      zh="第三，助焊剂。要保证助焊剂能够穿过整个通孔，到达顶面。", zh_sub="第三，助焊剂：要保证助焊剂能够穿过整个通孔，到达顶面。"),
 dict(scene=5, en="With enough heat in the hole, the solder keeps flowing and fills the hole to the top.",
      zh="孔里的热量足够了，焊锡就能继续向上流动，把通孔填满。"),
 dict(scene=6, en="Please check this joint by X-ray, not by eye. Measure the fill height on J one, pin two. It must be seventy-five percent or more.",
      en_sub="Please check this joint by X-ray, not by eye. Measure the fill height on J1 pin 2. It must be 75% or more.",
      zh="请用爱克斯光检查这个焊点，不要只靠目检。测量这个接地引脚的透锡高度，必须达到百分之七十五以上。",
      zh_sub="请用 X 光检查这个焊点，不要只靠目检。测量 J1 第 2 脚的透锡高度，必须 ≥ 75%。"),
 dict(scene=6, en="Send us the X-ray image with each lot.", zh="每一批出货，请附上爱克斯光照片。", zh_sub="每一批出货，请附上 X 光照片。"),
 dict(scene=7, en="To summarize: more preheat, longer contact time, flux through the hole, and X-ray proof of seventy-five percent fill.",
      en_sub="To summarize: more preheat, longer contact time, flux through the hole, and X-ray proof of 75% fill.",
      zh="总结一下：加强预热，延长接触时间，助焊剂穿透通孔，并用爱克斯光确认透锡率达到百分之七十五。",
      zh_sub="总结：加强预热，延长接触时间，助焊剂穿透通孔，并用 X 光确认透锡率 ≥ 75%。"),
 dict(scene=7, en="On our side, the next board revision adds thermal relief on this pin, to make it easier to solder. Thank you.",
      zh="我们这边，下一版电路板会在这个引脚上增加花焊盘，让它更容易焊接。谢谢。"),
]
if __name__ == "__main__":
    import json, subprocess, os, wave
    here = os.path.dirname(os.path.abspath(__file__))
    out = []
    t = 0.8                                  # lead-in
    GAP = 0.55
    for i, c in enumerate(CUES):
        d = {}
        for lang, model in (("en", "en_US-ryan-high"), ("zh", "zh_CN-huayan-medium")):
            f = f"{here}/audio/{lang}_{i:02d}.wav"
            if not os.path.exists(f):
                subprocess.run(["python3", "-m", "piper", "-m", f"{here}/../tts/{model}.onnx", "-f", f], input=c[lang].encode(), check=True, capture_output=True)
            w = wave.open(f); d[lang] = w.getnframes() / w.getframerate(); rate = w.getframerate(); w.close()
        dur = max(d.values())
        extra = 1.2 if (i + 1 < len(CUES) and CUES[i + 1]["scene"] != c["scene"]) else 0.0
        out.append(dict(i=i, scene=c["scene"], start=round(t, 3), dur=round(dur, 3), en=c.get("en_sub", c["en"]), zh=c.get("zh_sub", c["zh"]), en_len=round(d["en"], 2), zh_len=round(d["zh"], 2)))
        t += dur + GAP + extra
    total = round(t + 1.5, 2)
    json.dump(dict(cues=out, total=total), open(f"{here}/cues.json", "w"), ensure_ascii=False, indent=1)
    for o in out: print(o["i"], o["scene"], o["start"], o["dur"], o["en_len"], o["zh_len"])
    print("total", total)
