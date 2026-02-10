import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ShakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_shaking = False
        self.shake_timer = QTimer()
        self.shake_timer.timeout.connect(self.shake_step)
        self.original_pos = None
        self.shake_steps = 0
        self.max_shake_steps = 20  # 抖动总步数
        
    def initUI(self):
        # 设置窗口基本属性
        self.setWindowTitle('窗口抖动测试程序')
        self.setGeometry(300, 300, 400, 300)
        
        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题标签
        title_label = QLabel('窗口抖动效果测试')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 18px; font-weight: bold; margin: 20px;')
        layout.addWidget(title_label)
        
        # 添加说明标签
        info_label = QLabel('点击下方按钮测试窗口抖动效果，可以调整参数控制抖动强度')
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 添加抖动参数控制区域
        params_group = QGroupBox('抖动参数设置')
        params_layout = QGridLayout()
        
        # 抖动幅度设置
        params_layout.addWidget(QLabel('抖动幅度:'), 0, 0)
        self.amplitude_spin = QSpinBox()
        self.amplitude_spin.setRange(1, 50)
        self.amplitude_spin.setValue(10)
        self.amplitude_spin.setSuffix(' 像素')
        params_layout.addWidget(self.amplitude_spin, 0, 1)
        
        # 抖动持续时间设置
        params_layout.addWidget(QLabel('抖动时间:'), 1, 0)
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 10)
        self.duration_spin.setValue(3)
        self.duration_spin.setSuffix(' 秒')
        params_layout.addWidget(self.duration_spin, 1, 1)
        
        # 抖动频率设置
        params_layout.addWidget(QLabel('抖动频率:'), 2, 0)
        self.frequency_slider = QSlider(Qt.Horizontal)
        self.frequency_slider.setRange(1, 100)
        self.frequency_slider.setValue(50)
        self.frequency_slider.setTickPosition(QSlider.TicksBelow)
        self.frequency_slider.setTickInterval(10)
        params_layout.addWidget(self.frequency_slider, 2, 1)
        
        # 频率显示标签
        self.frequency_label = QLabel('50 Hz')
        params_layout.addWidget(self.frequency_label, 2, 2)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # 连接频率滑块变化事件
        self.frequency_slider.valueChanged.connect(self.update_frequency_label)
        
        # 添加抖动按钮
        self.shake_button = QPushButton('开始抖动窗口')
        self.shake_button.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        ''')
        self.shake_button.clicked.connect(self.start_shake)
        layout.addWidget(self.shake_button)
        
        # 添加抖动状态标签
        self.status_label = QLabel('窗口状态: 正常')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet('font-size: 14px; margin: 10px;')
        layout.addWidget(self.status_label)
        
        # 添加抖动次数统计
        self.shake_count = 0
        self.count_label = QLabel('抖动次数: 0')
        self.count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.count_label)
        
        # 添加底部信息
        bottom_label = QLabel('PyQt5 窗口抖动演示程序')
        bottom_label.setAlignment(Qt.AlignCenter)
        bottom_label.setStyleSheet('color: #666666; margin-top: 20px;')
        layout.addWidget(bottom_label)
        
        # 设置布局边距
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
    def update_frequency_label(self):
        """更新频率标签显示"""
        freq = self.frequency_slider.value()
        self.frequency_label.setText(f'{freq} Hz')
        
    def start_shake(self):
        """开始抖动窗口"""
        if self.is_shaking:
            return
            
        self.is_shaking = True
        self.shake_button.setEnabled(False)
        self.shake_button.setText('抖动中...')
        self.status_label.setText('窗口状态: 抖动中')
        self.status_label.setStyleSheet('font-size: 14px; margin: 10px; color: #FF5722;')
        
        # 保存原始位置
        self.original_pos = self.pos()
        
        # 获取参数值
        amplitude = self.amplitude_spin.value()
        duration = self.duration_spin.value() * 1000  # 转换为毫秒
        frequency = self.frequency_slider.value()
        
        # 计算抖动参数
        self.shake_steps = 0
        self.shake_amplitude = amplitude
        self.shake_duration = duration
        
        # 设置定时器间隔
        interval = 1000 // frequency  # 毫秒
        self.shake_timer.start(interval)
        
        # 更新抖动次数
        self.shake_count += 1
        self.count_label.setText(f'抖动次数: {self.shake_count}')
        
    def shake_step(self):
        """执行一次抖动步骤"""
        if self.shake_steps >= self.max_shake_steps:
            self.stop_shake()
            return
            
        # 计算当前抖动偏移
        # 使用正弦函数创建平滑的抖动效果
        progress = self.shake_steps / self.max_shake_steps
        damping = 1.0 - progress  # 逐渐减小振幅
        
        # 随机偏移
        x_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * damping
        y_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * damping
        
        # 应用偏移
        new_x = self.original_pos.x() + x_offset
        new_y = self.original_pos.y() + y_offset
        self.move(int(new_x), int(new_y))
        
        self.shake_steps += 1
        
        # 如果达到最大抖动步数，停止抖动
        if self.shake_steps >= self.max_shake_steps:
            self.shake_timer.stop()
            # 延迟一小段时间后恢复，让用户看到最终位置
            QTimer.singleShot(100, self.stop_shake)
    
    def stop_shake(self):
        """停止抖动并恢复窗口位置"""
        self.shake_timer.stop()
        if self.original_pos:
            self.move(self.original_pos)
        
        self.is_shaking = False
        self.shake_button.setEnabled(True)
        self.shake_button.setText('开始抖动窗口')
        self.status_label.setText('窗口状态: 正常')
        self.status_label.setStyleSheet('font-size: 14px; margin: 10px; color: #4CAF50;')
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.is_shaking:
            self.shake_timer.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 创建并显示窗口
    window = ShakeWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()