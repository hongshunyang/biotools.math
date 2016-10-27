# How to use 

## Python Version

* 2.7

## Python Dependencies

* Scipy

## Options

* -i input file to be used
* -s (x,y) need to be used by line
* -c first column need to be used (start 0)
* -t input file has title or no,also start row
* -o 1 表示rr的值大于-r 传递的值
* -x 1 表示r的值大于0
* -n 保留哪些行，用逗号分隔ps:减1

## Example

```shell
./app.py -i ../data/0505/2.csv -s 40(need x,y nums) -o 1(1:>rr;0:<rr) -r 0.5( rr) -x 1(1:r>0;0:r<0) -n 3,5 -c 1(start cols)  -t(start rows) 1
```
