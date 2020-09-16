import sys, getopt, cv2


'''
A ideia inicial era criar um programa de linha de comando
que pudesse ser chamado separadamente a qualquer hora e
quantas vezes quisesse, possibilitando a manipulação de mais
de 1 imagem. Mas como decidi usar venv, fiquei impossibilitado
de executar o script chamando o interpretador python da venv.
"-v":"Vertical Flip",
"-h":"Horizontal Flip",
"-n":"Negative",
"-b":"Blur",
"-g":"Gradient",
"-c":"Canny Edge",
"-C":"Contours"
'''
optlist, args = getopt.getopt(sys.argv[1:], 'vhnbgcC')
image = cv2.imread('Upload/'+args[0])

for o, a in optlist:
    if o == "-v":
        image = cv2.flip(image, 0)
    elif o == "-h":
        image = cv2.flip(image, 1)
    elif o == "-n":
        image = cv2.bitwise_not(image)
    elif o == "-b":
        image = cv2.blur(image,(50,50))
    elif o == "-g":
        image = cv2.Laplacian(image,cv2.CV_64F)
    elif o == "-c":
        image = cv2.Canny(image,128,255)
    elif o == "-C": #Sempre usar esta opção antes das outras
        im_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        (thresh, im_bw) = cv2.threshold(im_bw, 128, 255, 0)
        contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image, contours, -1, (0,255,0), 3)

cv2.imwrite('Processed_Images/'+args[0], image)