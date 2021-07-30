import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import argparse
import torchvision
'exec(%matplotlib inline)'
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torch
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import transforms,utils,datasets
from PIL import Image
from torch.autograd import Variable
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import torchvision.models as models
from sklearn.datasets import fetch_20newsgroups

import warnings
warnings.filterwarnings("ignore")

train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.492, 0.461, 0.417], [0.256, 0.248, 0.251])
    ])
val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.492, 0.461, 0.417], [0.256, 0.248, 0.251])
    ])

EPOCH = 10   #遍历数据集次数
pre_epoch = 0  # 定义已经遍历数据集的次数
BATCH_SIZE = 16      #批处理尺寸(batch_size)
LR = 0.001        #学习率

train_dir = "/home/bosonlee/data/mnist/train"
train_datasets = datasets.ImageFolder(train_dir,transform=train_transform)
train_dataloader = torch.utils.data.DataLoader(train_datasets,batch_size=BATCH_SIZE,shuffle=True)

val_dir = "/home/bosonlee/data/mnist/val"
val_datasets = datasets.ImageFolder(val_dir,transform=val_transform)
val_dataloader = torch.utils.data.DataLoader(val_datasets,batch_size=BATCH_SIZE,shuffle=True)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


'''
class MyDataset(Dataset):
	def __init__(self,path_dir,transform=None):
		self.path_dir = path_dir
		self.transform =transform
		self.images = os.listdir(self.path_dir)

	def __len__(self):
		return len(self.images)

	def __getitem__(self, index):
		image_index = self.images[index]
		img_path = os.path.join(self.path_dir,image_index)
		img = Image.open(img_path).convert('RGB')

		label = img_path.split('/')[-1].split('_')[0]
		if 'left' in label :
    			label = 1 
		elif 'right' in label:
    			label = 2
		else :
    			label = 0
		
		if self.transform is not None:
			img = self.transform(img)
		return img,label


from torchvision import transforms as T
transform = T.Compose([
 T.Resize(32), 
 T.CenterCrop(32), 
 T.ToTensor(), 
 T.Normalize(mean=[0.492, 0.461, 0.417], std=[0.256, 0.248, 0.251]) 
])
dataset = MyDataset("/home/bosonlee/data/mnist/3000arrow",transform=transform)
dataloader = DataLoader(dataset,batch_size=4,shuffle=True)

EPOCH = 10   #遍历数据集次数
pre_epoch = 0  # 定义已经遍历数据集的次数
BATCH_SIZE = 16      #批处理尺寸(batch_size)
LR = 0.001        #学习率

train_set, test_set = train_test_split(dataset, test_size=0.4, random_state=5)
train_set, val_set =train_test_split(train_set,test_size=0.5,random_state=5)

train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
test_loader = DataLoader(test_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_loader = DataLoader(val_set,batch_size=BATCH_SIZE,shuffle=True, num_workers=0)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def imshow(img):
	img = img / 2 + 0.5  # unnormalize
	npimg = img.numpy()
	plt.imshow(np.transpose(npimg, (1, 2, 0)))
	plt.show()

dataiter = iter(dataloader)
images, labels = dataiter.next()

imshow(torchvision.utils.make_grid(images))
for j in range(4):
    	if labels[j].item()==1:
    		print("左轉") 
	elif labels[j].item()==2:
    		print("右轉")
	else:
			print("直走")

'''
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        
         ## define the layers

        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)

        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)

        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)

        self.conv4 = nn.Conv2d(64, 128, 3, padding=1)

        self.conv5 = nn.Conv2d(128, 256, 3, padding=1)

        self.pool = nn.MaxPool2d(2, 2)

        self.linear1 = nn.Linear(256*7*7, 128)

        self.linear2 = nn.Linear(128, 3)

    

    def forward(self, x):

        x = self.pool(F.relu(self.conv1(x)))

        x = self.pool(F.relu(self.conv2(x)))

        x = self.pool(F.relu(self.conv3(x)))

        x = self.pool(F.relu(self.conv4(x)))

        x = self.pool(F.relu(self.conv5(x)))

        #print(x.shape)

        x = x.view(x.size(0),-1) 

        x = F.relu(self.linear1(x))

        x = self.linear2(x)

        return x
#net=Net()
#print(net)

#model_ft = models.resnet18(pretrained=True)
model = Net().to(device)
criterion = nn.CrossEntropyLoss()  #损失函数为交叉熵，多用于多分类问题
optimizer = optim.SGD(model.parameters(), lr=LR, momentum=0.9, weight_decay=5e-4) #优化方式为mini-batch momentum-SGD，并采用L2正则化（权重衰减）

def train (net,epoch):
    net.train()
    for batch_idx, (data,target) in enumerate(train_dataloader):
        data, target = Variable(data),Variable(target)
        optimizer.zero_grad()
        output = net(data)
        loss = F.cross_entropy(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 10 == 0:
            print('Train Epoch:{} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_dataloader.dataset),
                100. * batch_idx / len(train_dataloader), loss.item()))

def test(net):
    net.eval()
    test_loss = 0
    correct = 0
    for data,target in val_dataloader:
        data,target = Variable(data,volatile=True), Variable(target)
        output = net(data)
        test_loss += F.cross_entropy(output, target, size_average=False).item()
        pred = output.data.max(1,keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(val_dataloader.dataset)
    print('\nTest set:Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(val_dataloader.dataset),
        100. * correct / len(val_dataloader.dataset)))

for epoch in range(1, 8):
    train(model,epoch)
    test(model)
torch.save(model,'model.pkl')
'''
# 训练
if __name__ == "__main__":
	#if not os.path.exists(args.outf):
	#	os.makedirs(args.outf)
    best_acc = 0  #2 初始化best test accuracy
    print("Start Training!")  # 定义遍历数据集的次数
    with open("acc.txt", "w") as f:
        with open("log.txt", "w")as f2:
            for epoch in range(pre_epoch, EPOCH):
                print('\nEpoch: %d' % (epoch + 1))
                net.train()
                sum_loss = 0.0
                correct = 0.0
                total = 0.0
                for i, data in enumerate(train_dataloader, 0):
                    # 准备数据
                    length = len(train_loader)
                    inputs, labels = data
                    inputs, labels = inputs.to(device), labels.to(device)
                    optimizer.zero_grad()

                    # forward + backward
                    outputs = net(inputs)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()

                    # 每训练1个batch打印一次loss和准确率
                    sum_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += predicted.eq(labels.data).cpu().sum()
                    print('[epoch:%d, iter:%d] Loss: %.03f | Acc: %.3f%% '
                          % (epoch + 1, (i + 1 + epoch * length), sum_loss / (i + 1), 100. * correct / total))
                    f2.write('%03d  %05d |Loss: %.03f | Acc: %.3f%% '
                          % (epoch + 1, (i + 1 + epoch * length), sum_loss / (i + 1), 100. * correct / total))
                    f2.write('\n')
                    f2.flush()

                # 每训练完一个epoch测试一下准确率
                print("Waiting Test!")
                with torch.no_grad():
                    correct = 0
                    total = 0
                    for data in test_loader:
                        net.eval()
                        images, labels = data
                        images, labels = images.to(device), labels.to(device)
                        outputs = net(images)
                        # 取得分最高的那个类 (outputs.data的索引号)
                        _, predicted = torch.max(outputs.data, 1)
                        total += labels.size(0)
                        correct += (predicted == labels).sum()
                    print('測試分類準確率為：%.3f%%' % (100 * correct / total))
                    acc = 100. * correct / total
                    # 将每次测试结果实时写入acc.txt文件中
                    print('Saving model......')
                    #torch.save(net.state_dict(), '%s/net_%03d.pth' % (args.outf, epoch + 1))
                    f.write("EPOCH=%03d,Accuracy= %.3f%%" % (epoch + 1, acc))
                    f.write('\n')
                    f.flush()
                    # 记录最佳测试分类准确率并写入best_acc.txt文件中
                    if acc > best_acc:
                        f3 = open("best_acc.txt", "w")
                        f3.write("EPOCH=%d,best_acc= %.3f%%" % (epoch + 1, acc))
                        f3.close()
                        best_acc = acc
            print("Training Finished, TotalEPOCH=%d" % EPOCH)
#img, _ = test_set[0]
#net.eval()
#with torch.no_grad():
#    prediction = net([img.to(device)])
#print(prediction)
torch.save(net.state_dict(),'model.pt')
'''