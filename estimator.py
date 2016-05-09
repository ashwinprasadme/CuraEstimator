#!/usr/bin/env python
import os, sys
from settings import APP_STATIC,APP_UPLOAD,APP_SLIC3R
from subprocess import call, Popen
import gcoder
import rounder
import time
import send_email
import json

#system arguments
UPLOAD_FOLDER = APP_UPLOAD

def start_cura(filename,quality):
    output_file = os.path.splitext(os.path.join(UPLOAD_FOLDER, filename))[0] + ".gcode"
    print "output_file:" + output_file + "\n"
    config_file = os.path.join(APP_STATIC, quality) + ".ini"
    cura_settings = [os.path.join(APP_SLIC3R, "./CuraEngine"),"-c",config_file,"-o",output_file,os.path.join(UPLOAD_FOLDER, filename)]
    #Cura from filename
    print cura_settings

    slicer = call(cura_settings) #Blocking

    first, file_extension = os.path.splitext(filename)
    gcode_Sliced = first + '.gcode'
    print gcode_Sliced

    fname = os.path.join(UPLOAD_FOLDER, gcode_Sliced)

    # Gcode file analysis
    gcode = gcoder.GCode(open(fname, "rU"))
    # print gcode
    print "Dimensions:"
    xdims = (gcode.xmin, gcode.xmax, gcode.width)
    print "\tX: %0.02f - %0.02f (%0.02f)" % xdims
    ydims = (gcode.ymin, gcode.ymax, gcode.depth)
    print "\tY: %0.02f - %0.02f (%0.02f)" % ydims
    zdims = (gcode.zmin, gcode.zmax, gcode.height)
    print "\tZ: %0.02f - %0.02f (%0.02f)" % zdims
    print "Filament used: %0.02fmm" % gcode.filament_length
    print "Number of layers: %d" % gcode.layers_count
    print "Estimated duration: %s" % gcode.estimate_duration()[1]
    print "Estimated duration Hours: %0.02f" % gcode.duration_hours
    #round to 0.5
    dur_in_hours = rounder.round_to_5(gcode.duration_hours)
    if dur_in_hours == 0:
        dur_in_hours = 0.5
    #Multiply per hour cost
    cost = dur_in_hours*300
    print "\n"

    print_dict = {
        "price": str(cost),
        "width": gcode.width,
        "depth": gcode.depth,
        "height": gcode.height,
        "filament_length": "%0.02f" % gcode.filament_length,
        "print_time": "%0.02f" % dur_in_hours
    }
    print print_dict

    json_file = os.path.splitext(os.path.join(UPLOAD_FOLDER, filename))[0] + ".json"
    out_file = open(json_file,"w")
    json.dump(print_dict,out_file, indent=4)

    # Close the file
    out_file.close()

    # file.write(dumps({'numbers':n, 'strings':s, 'x':x, 'y':y}, file, indent=4))
    # with open("text", "w") as outfile:
    #     json.dump({'numbers':n, 'strings':s, 'x':x, 'y':y}, outfile, indent=4)



def start_slice(name, email, filename, quality, support, order_id):
    #name, email, filename, quality, speed, support

    #Construct Command
    output_file = os.path.splitext(os.path.join(UPLOAD_FOLDER, filename))[0] + ".gcode"
    print "output_file:" + output_file + "\n"
    config_file = os.path.join(APP_STATIC, quality) + ".ini"
    slicer_settings = [os.path.join(APP_SLIC3R, "./CuraEngine"),"-c",config_file,"-o",output_file,os.path.join(UPLOAD_FOLDER, filename)]
    #From Form
    # slicer_settings.append("-c")
    # slicer_settings.append("quality")
    # slicer_settings.append("--infill-speed")
    # slicer_settings.append(speed)
    # print support
    # if support == 'Yes' :
        # slicer_settings.append("--support-material")


    #Slic3r from filename
    print slicer_settings

    slicer = call(slicer_settings) #Blocking
    print "\n"

    first, file_extension = os.path.splitext(filename)
    gcode_Sliced = first + '.gcode'

    print gcode_Sliced

    fname = os.path.join(UPLOAD_FOLDER, gcode_Sliced)

    # Gcode file analysis
    gcode = gcoder.GCode(open(fname, "rU"))
    print gcode

    print "Dimensions:"
    xdims = (gcode.xmin, gcode.xmax, gcode.width)
    print "\tX: %0.02f - %0.02f (%0.02f)" % xdims
    ydims = (gcode.ymin, gcode.ymax, gcode.depth)
    print "\tY: %0.02f - %0.02f (%0.02f)" % ydims
    zdims = (gcode.zmin, gcode.zmax, gcode.height)
    print "\tZ: %0.02f - %0.02f (%0.02f)" % zdims
    print "Filament used: %0.02fmm" % gcode.filament_length
    print "Number of layers: %d" % gcode.layers_count
    print "Estimated duration: %s" % gcode.estimate_duration()[1]
    print "Estimated duration Hours: %s" % gcode.duration_hours
    #round to 0.5
    dur_in_hours = rounder.round_to_5(gcode.duration_hours)
    if dur_in_hours == 0:
        dur_in_hours = 0.5
    #Multiply per hour cost
    cost = dur_in_hours*300
    print "\n"

    # Mail
    send_email.send_estimation(email,gcode.estimate_duration()[1],cost,name,filename,order_id)

if __name__ == "__main__":
    #name, email, filename, quality, speed, support
   # start_slice(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])

   # filename, quality
   start_cura(sys.argv[1],sys.argv[2])
