import csv, queue, time
from sys import argv
from sudoku.sudoku import SudokuCheckQuestion, Sudoku


def read_csv(path):
    with open(path, 'r') as f:
        d = [[int(v.replace(' ', '')) for v in row] for row in csv.reader(f)]
    return d


def main(d):
    start_time = time.time()
    question = SudokuCheckQuestion(d)
    question.verbose = True
    if question.get_valid():
        print('The question is ...')
        question.print_question()
        lifo_q = queue.LifoQueue()
        for i in range(question.get_size(), 0, -1):
            q = Sudoku(question.get_question())
            q.set_next_value(i)
            lifo_q.put(q)

        counter = 0
        could_solve = False
        while lifo_q:
            q = lifo_q.get(timeout=3)
            if q.check_insert():
                q.set_next_value_to_question()
                counter += 1
                if q.check_complete():
                    could_solve = True
                    print('\nThe answer is ...')
                    q.print_question()
                    print(f'counter: {counter}')

                    end_time = time.time()

                    exec_time = end_time - start_time
                    print(f'exec time: {str(exec_time)}')

                    break
                for i in range(question.get_size(), 0, -1):
                    q = Sudoku(q.get_question())
                    q.set_next_value(i)
                    lifo_q.put(q)
        if not could_solve:
            print('It could not resolved')
            return False
    else:
        print('This question is invalid')
        return False


if __name__ == '__main__':
    data = read_csv(argv[1])
    main(data)


