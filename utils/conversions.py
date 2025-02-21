def convert_pixel_to_actual(pixel_distance,reference_h_act,reference_h_pix):
    return pixel_distance*(reference_h_act/reference_h_pix)

def convert_actual_to_pixel(actual_distance,reference_h_act,reference_h_pix):
    return actual_distance*(reference_h_pix/reference_h_act)

