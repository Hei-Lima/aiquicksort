import random
import google.generativeai as genai
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging

# Api Key goes Here:
GOOGLE_API_KEY = ""

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-lite')

def clean_response(response):
    for i in response:
        if i == '1':
            return 1
    return 2

def qsort(list_data, ptr_esq=0, ptr_dir=None):
    if ptr_dir is None:
        ptr_dir = len(list_data) - 1

    if ptr_esq < ptr_dir:
        ind_pivo = random.randint(ptr_esq, ptr_dir)
        esq = ptr_esq + 1
        dir = ptr_dir
        
        list_data[ind_pivo], list_data[ptr_esq] = list_data[ptr_esq], list_data[ind_pivo]
        
        while esq <= dir:
            # Find element greater than the pivot on the left side
            while esq <= dir and is_left_smaller(list_data[esq], list_data[ptr_esq]):
                esq += 1
            
            # Find element smaller than the pivot on the right side
            while esq <= dir and not is_left_smaller(list_data[dir], list_data[ptr_esq]):
                dir -= 1
            
            if esq < dir:
                list_data[esq], list_data[dir] = list_data[dir], list_data[esq]
        
        # Place the pivot in its final position
        list_data[ptr_esq], list_data[dir] = list_data[dir], list_data[ptr_esq]
        
        qsort(list_data, ptr_esq, dir - 1)
        qsort(list_data, dir + 1, ptr_dir)

def is_left_smaller(esq, dir):
    sides = (("Left", esq), ("Right", dir))
    prompt = f"Which of these two elements is smaller? {esq} or {dir}? The first one or the second one? If it is the first one, please only respond with '1', else respond with '2'."
    response = model.generate_content(prompt)
    response = clean_response(response.text)
    
    if response == 1:
        print(f"The model thinks that {sides[0][1]} ({sides[0][0]}) is smaller than {sides[1][1]} ({sides[1][0]})")
        return True
    else:
        print(f"The model thinks that {sides[1][1]} ({sides[1][0]}) is smaller than {sides[0][1]} ({sides[0][0]})")
        return False

def main():
    list_data = [1, 3, 2, 6, 4, 5]
    qsort(list_data)
    print(f"THE SORTED LIST = {list_data}")

if __name__ == "__main__":
    main()