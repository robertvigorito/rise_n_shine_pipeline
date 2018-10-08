import nuke


def proxy_render(file_directory, shot_number, shot_name, main_plate=True, proxy=True):
    sel = nuke.selectedNode()
    if sel and sel.Class() == 'Read':
        active_viewer = nuke.activeViewer().node()
        # Define xpos, ypos and frame range
        xpos, ypos = sel.xpos(), sel.ypos()

        # Update frame range to in and out
        frame_range = active_viewer['frame_range'].getValue()
        first_frame, last_frame = int(frame_range.split('-')[0]), int(frame_range.split('-')[1])
        frame_offset = 1001 - first_frame
        last_frame = last_frame + frame_offset

        # Create time offset
        time_offset = nuke.nodes.TimeOffset(time_offset=frame_offset)
        time_offset.setInput(0, sel)

        # Create updated frame range
        frame_range = nuke.nodes.FrameRange(first_frame=1001, last_frame=last_frame)
        frame_range.setInput(0, time_offset)
        last_node = frame_range

        # Create Crop on Anamorphic Plate
        if sel.format().r() == 3792:
            crop = nuke.nodes.Crop(reformat=True, crop=False)
            crop['box'].setValue([0, 790, 3792, 2370])
            crop.setInput(0, last_node)
            last_node = crop

        # Create dot breaker for proxy render
        dot = nuke.nodes.Dot()
        dot.setInput(0, last_node)
        dot.setXYpos(xpos + 33, ypos + 200)

        dot1 = nuke.nodes.Dot()
        dot1.setInput(0, dot)
        dot1.setXYpos(xpos + 200, ypos + 200)

        # Create Write Node
        write = nuke.nodes.Write(file_type='exr', create_directories=True)
        write['file'].setValue(file_directory + '{}/{}_Plate.%0d.exr'.format(shot_name, shot_number))
        write.setInput(0, dot)
        write.setYpos(write.ypos() + 100)

        # Create Reformat Node
        reformat = nuke.nodes.Reformat(type=1, box_width=1920)
        reformat.setInput(0, dot1)
        reformat.setYpos(reformat.ypos() + 40)

        write1 = nuke.nodes.Write(file_type='exr', create_directories=True)
        write1['file'].setValue(file_directory + '{} Proxy/{}_Proxy.%0d.exr'.format(shot_name, shot_number))
        write1.setInput(0, reformat)
        write1.setYpos(write1.ypos() + 35)

        # Render elements
        if main_plate:
            nuke.execute(write, 1001, last_frame)
        if proxy:
            nuke.execute(write1, 1001, last_frame)
        return



