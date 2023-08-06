# PyQt5 �������

## ��飺

����pyqtSlot+QMutex+QThread+pyqtSignal�з��Ķ��߳�ʹ�ÿ�ܡ�
https://pypi.org/project/PyQt5-comet/

## ��װ������
```shell script
pip install -i https://test.pypi.org/simple/ PyQt5-comet --prefix="�ҵ���Ŀ·��"
����Lib\site-packages\PyLib��Lib\site-packages\main.py����Ŀ��Ŀ¼�����ɿ�ʼʹ�á�
```

## ��Ҫ֧��ģ�飺
```shell script
pip install pyqt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pyqt5-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## ��װ�̳̣�

����ִ�а�װPyQt5ģ�顣
```shell script
pip install pyqt5 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install pyqt5-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
```

Ȼ��ִ�У�
```shell script
pip install -i https://test.pypi.org/simple/ PyQt5-comet --prefix="�ҵ���Ŀ·��"
or
pip install PyQt5-comet --prefix="�ҵ���Ŀ·��"
```

���Lib\site-packages\PyLib��Lib\site-packages\main.py���Ƶ���Ŀ��Ŀ¼��

## ʹ�ý̳�

### Ŀ¼�ṹΪ��
```
-PyLib
    Controller.py
    MainUi.py
    Module-Test.py
    ProgramManagement.py
    MainUi.ui
main.py
```

### ģ����ܣ�
main.py ����GUI <br>
Controller.py ������<br>
MainUi.py GUI����<br>
Module-Test.py ����ģ��<br>
ProgramManagement.py ���̺߳�ģ�������<br>

### �����̳�

��������Ҫ��ɵ��߼����̶�class RunModule ����update ����ֵΪ�ַ���������ΪModule-Test.py�ļ���

```python
import _thread
import os

class RunModule:
    def __init__(self, tmp_dict):
        self.log = tmp_dict.get("log")
        pass

    def _log(self,threadName):
        print(os.getpid())
        print(self.log)
        print(threadName)

    def run(self):
        _thread.start_new_thread(self._log,("Thread-1",))

    def update(self):
        self.run()
        return self.log
        pass
```

�ڿ������м��أ�name="Module-Test" ����Ҫ���ص�ģ�����ƣ�log=str("TEST LOG PRINT") �Ǵ��ݵĲ�����<br>
connect(self._lookTestsLog)�ǻص�������<br>
ע���������ù淶 on_�������_�������() �����Ϳ���ͨ��װ����������������Ͷ�����

```python
    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.q.lock()
        self.runCmd_ = runCmd(name="Module-Test", log=str("TEST LOG PRINT"))
        self.runCmd_.cmdsign.connect(self._lookTestsLog)
        self.runCmd_.start()
        self.runCmd_.wait()
        self.q.unlock()
    def _lookTestsLog(self, log):
        self.label.setText(log)
```

�������main.py���ɡ�
