def bdy_str(A, B):
    if len(A) != len(B):
        return False

    import numpy as np
    from collections import Counter

    a = np.array(list(A))
    b = np.array(list(B))
    ct = 0
    cond = False
    tempi = []

    for i in range(len(a)):
        try:
            if a[i] != b[i]:
                ct += 1
                tempi.append(i)
        except:
            pass
        if ct > 2:
            cond = False
            break

    try:
        if ct == 0 and Counter(a).most_common(1)[0][1] > 1:
            cond = True
        elif ct == 2:
            temp = a[tempi[0]]
            a[tempi[0]] = a[tempi[1]]
            a[tempi[1]] = temp
            if a[tempi[0]] == b[tempi[0]] and a[tempi[1]] == b[tempi[1]]:
                cond = True
    except:
        pass
    return cond


print(bdy_str("aaaaa", "aaaab"))



