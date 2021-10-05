import torch
import string

all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)

all_categories = ['Arabic','Chinese','Czech','Dutch','English','French','German','Greek',
                'Irish','Italian','Japanese','Korean','Polish','Portuguese','Russian','Scottish',
                'Spanish','Vietnamese']

# Find letter index from all_letters: Ex: "a" = 0
def letterToIndex(letter):
    return all_letters.find(letter)

# Giving each charachter in name a one hot vector
def lineToTensor(line):
    tensor = torch.zeros(len(line),1,n_letters)
    for li,letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1

    return tensor 

# Loading in torchscript model
my_model = torch.jit.load('name_classifier_ts.pt')
# Return output given a line_tensor
def evaluate(line_tensor):
    hidden = torch.zeros(1,128)

    for i in range(line_tensor.size()[0]):
        output, hidden = my_model(line_tensor[i], hidden)

    return output

# Feeding in a name and number of top predictions you want to output
def predict(input_line,n_predictions=3):
    #print('Name:',input_line)
    with torch.no_grad():
        output = evaluate(lineToTensor(input_line))
        
        topv,topi = output.topk(n_predictions,1,True)
        
        output_tuples = []
        for i in range(n_predictions):
            value = topv[0]
            category_index = topi[0][i].item()
            output_tuples.append((all_categories[category_index],round(torch.exp(value[i]).item()*100,2)))
            #print(f'{all_categories[category_index]}: {round(torch.exp(value[i]).item()*100,2)}%')
    #print('\n')
    return output_tuples
