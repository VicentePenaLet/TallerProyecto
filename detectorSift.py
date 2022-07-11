import numpy as np
import pandas as pd
import cv2


# funcion para crear base de datos con caracteristicas sift
def extract_sift_df(df, name_df):
    new_df = []
    sift = cv2.SIFT_create()
    for i in range(len(df)):
        img1 = cv2.imread(f"DB_Galletas\{df[i][0]}",cv2.IMREAD_GRAYSCALE)         
        img1 = cv2.blur(img1, (3, 3))     
        kp1, des1 = sift.detectAndCompute(img1,None)
        new_df.append([df[i][0],des1])
        new_df = np.asarray(new_df,dtype=object)
        with open(f'{name_df}.npy', 'wb') as f:
            np.save(f, new_df)
    #return np.asarray(new_df,dtype=object)


# funcion para extraer caracteristicas Sift de una imagen
def extract_sift(img):
    sift = cv2.SIFT_create()
    # img1 = cv2.imread(img,cv2.IMREAD_GRAYSCALE)         
    img1 = cv2.blur(img, (3, 3))     
    kp1, des1 = sift.detectAndCompute(img1,None)
    return kp1, des1


def add_id(df,id):
    for i in range(len(df)):
        df.iloc[i,0] = f"{id}{df.iloc[i,0]+1}"
        #df.iloc[i,0] = f"{id}-{df.iloc[i,0]+1}"
    return df


# funcion para buscar imagen en la base
def search_img_in_db(img, df, db, threshold):
    MIN_MATCH_COUNT = 10
    kp1, des1 = extract_sift(img)
    good2 = []
    for i in range(len(df)):
        # kp2, des2 = df[i][2], df[i][3]
        des2 = df[i][1]
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2,k=2)
        # Apply ratio test
        good = []
        for m,n in matches:
            if m.distance < threshold*n.distance:
                good.append([m])
            
        if len(good) > MIN_MATCH_COUNT:
            #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            good2.append([df[i][0],len(good)])
            
    sorted_good = sorted(good2, key=lambda x:x[1])
    best_match = sorted_good[-1]
    #return best_match
    return db[db["Product Id"] == best_match[0][:-4]]

    