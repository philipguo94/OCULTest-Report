'''
    Author: Philip Guo
    Email: yawenguo@connect.hku.hk
    CopyRight: ACE Virtual Reality Ltd.
    Date created: 9/12/2020
    Date last modified: 05/10/2021
    Python Version: 3.7
    Description: 
    This is the main script to generate Visual Disability report to evaluate visual disability perofrmance for patients.
    The corrsponding work are finished in Deparment of Visual Science and Ophthalmology and Hong Kong Eye Hosptial, and 
    the copyright belongs to ACE Virtual Reality Ltd.
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D, art3d
import scipy.io as scio

from utils.scoring_2d import rangeplot_3d
from utils.vr_score import cal_score


def hidden_axis(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)


def generate_report(test_type, ID, age, duration, wrong_num, path, txt_file_name, date_time):
    '''
    Input:
        test_type (string): 'Supermarket' or 'City Navigation - Night' or 'City Navigation - Day'
        ID (string): patient_id  'HKE001'
        age (int): '20'
        duration (float): '30.2'
        wrong_num (int): the wrong select choice or hit time 
        path (string): the full path of the folder to save reports 
        txt_file_name(string): the name of the target txt or csv file generated from Unity demo
        date_time (string or date type): the test date '2012-01-01'
        
    Return:
        no returns, but generate reports into target folder
    '''
    
    
    print('Test Type: ', test_type)
    
    # load the coresponding parameters according to the test type
    if test_type == 'Supermarket':
        v = np.array(scio.loadmat('./utils/cr.mat')["cr"])
        for i in range(len(v)):
            if v[i][2]<0:
                v[i][2]=0
        f= np.array(scio.loadmat('./utils/F.mat')["F"])-1
        C= np.array(scio.loadmat('./utils/col.mat')["col"])
        C= C.reshape(len(C))
        line3ds_h = np.array(scio.loadmat('./utils/save_cr_line_h.mat')["save_cr_line"])
        line3d_v = np.array(scio.loadmat('./utils/save_cr_line_v.mat')["save_cr_line"])
        wrong_num = wrong_num - 10

    elif test_type == 'City Navigation - Night':
        v = np.array(scio.loadmat('./utils/cr_city_night.mat')["cr"])
        for i in range(len(v)):
            if v[i][2]<0:
                v[i][2]=0
        f= np.array(scio.loadmat('./utils/F_city_night.mat')["F"])-1
        C= np.array(scio.loadmat('./utils/col_city_night.mat')["col"])
        C= C.reshape(len(C))
        line3ds_h = [np.array([scio.loadmat('./utils/save_cr_line_h_city_night.mat')["cr2_output_"]])]
        line3d_v = np.array(scio.loadmat('./utils/save_cr_line_v_city_night.mat')["cr1_output"])

    elif test_type == 'City Navigation - Day':
        v = np.array(scio.loadmat('./utils/cr_city_day.mat')["cr"])
        for i in range(len(v)):
            if v[i][2]<0:
                v[i][2]=0
        f= np.array(scio.loadmat('./utils/F_city_day.mat')["F"])-1
        C= np.array(scio.loadmat('./utils/col_city_day.mat')["col"])
        C= C.reshape(len(C))
        line3ds_h = [np.array([scio.loadmat('./utils/save_cr_line_h_city_day.mat')["cr2_output_"]])]
        line3d_v = np.array(scio.loadmat('./utils/save_cr_line_v_city_day.mat')["cr1_output"])

    elif test_type == 'Stair Navigation - Night':
        v = np.array(scio.loadmat('./utils/cr_stair_night.mat')["cr"])
        for i in range(len(v)):
            if v[i][2]<0:
                v[i][2]=0
        f= np.array(scio.loadmat('./utils/F_stair_night.mat')["F"])-1
        C= np.array(scio.loadmat('./utils/col_stair_night.mat')["col"])
        C= C.reshape(len(C))
        line3ds_h = [np.array([scio.loadmat('./utils/save_cr_line_h_stair_night.mat')["cr2_output_"]])]
        line3d_v = np.array(scio.loadmat('./utils/save_cr_line_v_stair_night.mat')["cr1_output"])

    elif test_type == 'Stair Navigation - Day':
        v = np.array(scio.loadmat('./utils/cr_stair_day.mat')["cr"])
        for i in range(len(v)):
            if v[i][2]<0:
                v[i][2]=0
        f= np.array(scio.loadmat('./utils/F_stair_day.mat')["F"])-1
        C= np.array(scio.loadmat('./utils/col_stair_day.mat')["col"])
        C= C.reshape(len(C))
        line3ds_h = [np.array([scio.loadmat('./utils/save_cr_line_h_stair_day.mat')["cr2_output_"]])]
        line3d_v = np.array(scio.loadmat('./utils/save_cr_line_v_stair_day.mat')["cr1_output"])


    # vertical lines
    line3d_v = list(line3d_v)
    line3ds_v = []
    idx = 1
    temp_arr = [line3d_v[0]]
    while idx < len(line3d_v):
        if line3d_v[idx][2] < 0:
            line3d_v.pop(idx)
            continue
        else:
            if line3d_v[idx][0]==line3d_v[idx-1][0]:
                temp_arr.append(line3d_v[idx])
                idx+=1
            else:
                line3ds_v.append(temp_arr)
                temp_arr = []
                idx+=1


    # generate the overlay of the report
    fig = plt.figure(figsize=(6,8),num='VR Supermarket Report')     
    fig.subplots_adjust(left=0.05, bottom=0.03, right=0.95, top=0.97)   


    # the 3d Plot    
    ax = fig.add_subplot(212,projection="3d")
    norm = plt.Normalize(C.min(), C.max())
    colors = plt.cm.viridis(norm(C))
    
    
    # 3d surface
    pc = art3d.Poly3DCollection(v[f], facecolors='red',linewidths=1,alpha=0.2)
    ax.add_collection(pc)


    # vertical line on surface
    for line3d in line3ds_v:
        line3d = np.array(line3d)
        ax.plot(line3d[:,0],line3d[:,1],line3d[:,2],zdir='z',color='grey',linewidth=0.3, alpha=0.1)


    # horizontal line on surface
    for line3d in line3ds_h:
        line3d_ = np.array(line3d)[0]
        print(line3d_)
        for i in range(0,len(line3d_),2):
            line3d = line3d_[i:i+2]
            print(line3d)
            if line3d[0][2]>0 and line3d[1][2]>0:
                ax.plot(line3d[:,0],line3d[:,1],line3d[:,2],zdir='z',color='grey',linewidth=0.3, alpha=0.1)


    # center-line, black
    ax.plot([line3ds_h[0][0][0,0]],[line3ds_h[0][0][0,1]],[line3ds_h[0][0][0,2]],zdir='z',color='black',alpha=1)


    # generate the marker
    print(age, duration, wrong_num)
    ax.scatter([age],[duration],[wrong_num],color='black')


    # adjust the axis displaying ranges according to different types 
    if test_type == 'Supermarket':
        ax.set_xlim(0,100)
        ax.set_ylim(0,200)
        ax.set_zlim(0,8)
        ax.set_yticks(np.arange(0, 200, 50))
    elif test_type == 'City Navigation - Night':
        ax.set_xlim(0,100)
        ax.set_ylim(0,300)
        ax.set_zlim(0,5)
        ax.set_yticks(np.arange(0, 400, 100))
    elif test_type == 'Stair Navigation - Night':
        ax.set_xlim(0,100)
        ax.set_ylim(0,500)
        ax.set_zlim(0,8)
        ax.set_yticks(np.arange(0, 600, 100))
    elif test_type == 'City Navigation - Day':
        ax.set_xlim(0,100)
        ax.set_ylim(0,300)
        ax.set_zlim(0,5)
        ax.set_yticks(np.arange(0, 400, 100))
    elif test_type == 'Stair Navigation - Day':
        ax.set_xlim(0,100)
        ax.set_ylim(0,500)
        ax.set_zlim(0,8)
        ax.set_yticks(np.arange(0, 600, 100))


    # set the labels for each axies
    ax.set_xlabel("Age")
    ax.set_ylabel("Task Duration(s)")
    ax.set_ylim(ax.get_ylim()[::-1])
    if test_type == 'Supermarket':
        ax.set_zlabel("No. of Wrong Choice")
    elif test_type == 'City Navigation - Night':
        ax.set_zlabel("No. of Collision")
    elif test_type == 'Stair Navigation - Night':
        ax.set_zlabel("No. of Collision")
    elif test_type == 'City Navigation - Day':
        ax.set_zlabel("No. of Collision")
    elif test_type == 'Stair Navigation - Day':
        ax.set_zlabel("No. of Collision")


    # ACEVR logo
    img = Image.open('./asset/acevr_logo.png')
    ax2 = fig.add_subplot(915)
    ax2.imshow(img)
    hidden_axis(ax2)


    # report title
    font = {'weight': 'bold',
            'size': 14,
            }
    ax3 = fig.add_subplot(611)
    ax3.text(.2, .85, 'VR Visual Performance Report', fontdict=font, ha='left', wrap=True)
    if test_type == 'Supermarket':
        ax3.text(.25, .50, '        (' + test_type + ')', fontdict=font, ha='left', wrap=True)
    elif test_type == 'City Navigation - Night' or 'City Navigation - City':
        ax3.text(.25, .50, '(' + test_type + ')', fontdict=font, ha='left', wrap=True)
    elif test_type == 'Stair Navigation - Night' or 'Stair Navigation - City':
        ax3.text(.25, .50, '(' + test_type + ')', fontdict=font, ha='left', wrap=True)
    hidden_axis(ax3)


    # Patient Infomation
    ax5 = fig.add_subplot(712)
    ax5.text(.1, .9, 'Patient ID: ' + str(ID), fontsize=11)
    ax5.text(.7, .9, 'Age: ' + str(age), fontsize=11)
    ax5.text(.1, .60, 'Test Time: ' + str(date_time), fontsize=11)
    hidden_axis(ax5)


    # 2D score
    score,_,threshold = cal_score(test_type, age, duration, wrong_num)
    score = round(score, 2)
    score_img_2d = rangeplot_3d(test_type, score, threshold)
    score_img_2d = cv2.resize(score_img_2d, (2000,550))
    ax4 = fig.add_subplot(512)
    ax4.imshow(score_img_2d)
    hidden_axis(ax4)
    
    
    # output the report
    saved_img_path = path+'/' + txt_file_name[:-4].replace('SaveData',ID) + '_report.png'
    plt.savefig(saved_img_path, dpi=500)
    plt.cla()
    plt.clf()
    plt.close()
    im = Image.open(saved_img_path)
    im = np.array(im)
    canvas_new = im.copy()*0
    canvas_new[:1600,:,:] = im[:1600,:,:]
    canvas_new[1600:3300,:,:] = im[2300:4000,:,:]
    logo_resize = Image.open('./asset/acevr_logo.png').resize((3000,660))
    logo_resize = np.array(logo_resize)
    logo_resize = Image.fromarray(logo_resize)
    im = Image.fromarray(canvas_new)
    im.paste(logo_resize,(0,3300))
    im.save(saved_img_path)
    return


# local test for generate_report function
if __name__ == '__main__':
    generate_report('Stair Navigation - Night', 'Philip', 30, 43, 1, './x/x/x', './x/x/x', '2012-01-01')