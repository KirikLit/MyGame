def direction(obj1, obj2):
    if obj1.rect.x < obj2.rect.x and obj2.direction == -1:
        return True
    elif obj1.rect.x > obj2.rect.x and obj2.direction == 1:
        return True
    else:
        return False
