import cv2

def template_match(template, target, method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
    """
    Perform template matching 
    """
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(target_gray, template_gray, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        template_height, template_width = template_gray.shape[:2]
        
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        return [(top_left, bottom_right, 0)]  
    else:
        return []