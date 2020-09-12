# openSFMEx

数据处理流程图
``` flow
st=>start: 解析
op=>operation: Your Operation
cond=>condition: Yes or No?
e=>end
st->op->cond
cond(yes)->e
cond(no)->op