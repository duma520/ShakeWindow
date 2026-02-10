import sys
import random
import math
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
        self.max_shake_steps = 40  # 增加抖动总步数，使效果更明显
        
    def initUI(self):
        # 设置窗口基本属性
        self.setWindowTitle('窗口抖动测试程序 - 增强版')
        self.setGeometry(300, 300, 500, 400)
        
        # 创建中央部件和主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加标题标签
        title_label = QLabel('窗口抖动效果测试 - 增强版')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 20px; font-weight: bold; margin: 20px; color: #2196F3;')
        layout.addWidget(title_label)
        
        # 添加说明标签
        info_label = QLabel('点击下方按钮测试窗口抖动效果，可以调整参数控制抖动强度\n增强版提供了更大的参数范围，效果更明显')
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet('margin: 10px;')
        layout.addWidget(info_label)
        
        # 添加抖动参数控制区域
        params_group = QGroupBox('抖动参数设置（增强范围）')
        params_group.setStyleSheet('QGroupBox { font-weight: bold; }')
        params_layout = QGridLayout()
        
        # 抖动幅度设置 - 增强到最大200像素
        params_layout.addWidget(QLabel('抖动幅度:'), 0, 0)
        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider.setRange(5, 200)  # 增强范围：5-200像素
        self.amplitude_slider.setValue(30)
        self.amplitude_slider.setTickPosition(QSlider.TicksBelow)
        self.amplitude_slider.setTickInterval(20)
        params_layout.addWidget(self.amplitude_slider, 0, 1)
        
        # 幅度显示标签
        self.amplitude_label = QLabel('30 像素')
        self.amplitude_label.setStyleSheet('font-weight: bold;')
        params_layout.addWidget(self.amplitude_label, 0, 2)
        
        # 抖动持续时间设置 - 增强到最大30秒
        params_layout.addWidget(QLabel('抖动时间:'), 1, 0)
        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setRange(1, 30)  # 增强范围：1-30秒
        self.duration_slider.setValue(5)
        self.duration_slider.setTickPosition(QSlider.TicksBelow)
        self.duration_slider.setTickInterval(5)
        params_layout.addWidget(self.duration_slider, 1, 1)
        
        # 持续时间显示标签
        self.duration_label = QLabel('5 秒')
        self.duration_label.setStyleSheet('font-weight: bold;')
        params_layout.addWidget(self.duration_label, 1, 2)
        
        # 抖动频率设置 - 增强到最大200Hz
        params_layout.addWidget(QLabel('抖动频率:'), 2, 0)
        self.frequency_slider = QSlider(Qt.Horizontal)
        self.frequency_slider.setRange(10, 200)  # 增强范围：10-200Hz
        self.frequency_slider.setValue(80)
        self.frequency_slider.setTickPosition(QSlider.TicksBelow)
        self.frequency_slider.setTickInterval(20)
        params_layout.addWidget(self.frequency_slider, 2, 1)
        
        # 频率显示标签
        self.frequency_label = QLabel('80 Hz')
        self.frequency_label.setStyleSheet('font-weight: bold;')
        params_layout.addWidget(self.frequency_label, 2, 2)
        
        # 抖动模式选择
        params_layout.addWidget(QLabel('抖动模式:'), 3, 0)
        self.shake_mode = QComboBox()
        self.shake_mode.addItems(['随机抖动', '水平抖动', '垂直抖动', '圆形抖动', '地震模式'])
        params_layout.addWidget(self.shake_mode, 3, 1, 1, 2)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # 连接滑块变化事件
        self.amplitude_slider.valueChanged.connect(self.update_amplitude_label)
        self.duration_slider.valueChanged.connect(self.update_duration_label)
        self.frequency_slider.valueChanged.connect(self.update_frequency_label)
        
        # 添加预设按钮区域
        preset_group = QGroupBox('快速预设')
        preset_layout = QHBoxLayout()
        
        # 创建预设按钮
        mild_btn = QPushButton('轻微抖动')
        mild_btn.clicked.connect(lambda: self.set_preset(10, 3, 30))
        preset_layout.addWidget(mild_btn)
        
        medium_btn = QPushButton('中等抖动')
        medium_btn.clicked.connect(lambda: self.set_preset(50, 5, 60))
        preset_layout.addWidget(medium_btn)
        
        strong_btn = QPushButton('强烈抖动')
        strong_btn.clicked.connect(lambda: self.set_preset(100, 8, 100))
        preset_layout.addWidget(strong_btn)
        
        extreme_btn = QPushButton('极限抖动')
        extreme_btn.clicked.connect(lambda: self.set_preset(200, 15, 200))
        preset_layout.addWidget(extreme_btn)
        
        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)
        
        # 添加抖动按钮
        button_layout = QHBoxLayout()
        
        self.shake_button = QPushButton('🚀 开始抖动窗口')
        self.shake_button.setStyleSheet('''
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        ''')
        self.shake_button.clicked.connect(self.start_shake)
        button_layout.addWidget(self.shake_button)
        
        # 添加停止按钮
        self.stop_button = QPushButton('⏹ 停止抖动')
        self.stop_button.setStyleSheet('''
            QPushButton {
                background-color: #FF5722;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #E64A19;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        ''')
        self.stop_button.clicked.connect(self.stop_shake)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
        
        # 添加进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # 添加抖动状态标签
        self.status_label = QLabel('窗口状态: 正常')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet('font-size: 16px; margin: 10px; padding: 10px; background-color: #E8F5E9; border-radius: 5px;')
        layout.addWidget(self.status_label)
        
        # 添加抖动次数统计
        stats_layout = QHBoxLayout()
        
        self.shake_count = 0
        self.count_label = QLabel('抖动次数: 0')
        self.count_label.setStyleSheet('font-size: 14px; padding: 5px;')
        stats_layout.addWidget(self.count_label)
        
        # 添加最大偏移显示
        self.max_offset_label = QLabel('最大偏移: 0 像素')
        self.max_offset_label.setStyleSheet('font-size: 14px; padding: 5px;')
        stats_layout.addWidget(self.max_offset_label)
        
        # 添加总抖动时间显示
        self.total_time_label = QLabel('总抖动时间: 0 秒')
        self.total_time_label.setStyleSheet('font-size: 14px; padding: 5px;')
        stats_layout.addWidget(self.total_time_label)
        
        layout.addLayout(stats_layout)
        
        # 添加底部信息
        bottom_label = QLabel('增强版窗口抖动演示程序 | 参数范围大幅增强 | 提供多种抖动模式')
        bottom_label.setAlignment(Qt.AlignCenter)
        bottom_label.setStyleSheet('color: #666666; margin-top: 20px; font-style: italic;')
        layout.addWidget(bottom_label)
        
        # 设置布局边距
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 初始化统计变量
        self.total_shake_time = 0
        self.max_offset = 0
        
    def update_amplitude_label(self):
        """更新幅度标签显示"""
        amplitude = self.amplitude_slider.value()
        self.amplitude_label.setText(f'{amplitude} 像素')
        
    def update_duration_label(self):
        """更新持续时间标签显示"""
        duration = self.duration_slider.value()
        self.duration_label.setText(f'{duration} 秒')
        
    def update_frequency_label(self):
        """更新频率标签显示"""
        freq = self.frequency_slider.value()
        self.frequency_label.setText(f'{freq} Hz')
        
    def set_preset(self, amplitude, duration, frequency):
        """设置预设参数"""
        self.amplitude_slider.setValue(amplitude)
        self.duration_slider.setValue(duration)
        self.frequency_slider.setValue(frequency)
        
    def start_shake(self):
        """开始抖动窗口"""
        if self.is_shaking:
            return
            
        self.is_shaking = True
        self.shake_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.shake_button.setText('抖动中...')
        self.status_label.setText('窗口状态: 抖动中')
        self.status_label.setStyleSheet('font-size: 16px; margin: 10px; padding: 10px; background-color: #FFECB3; border-radius: 5px; color: #FF5722;')
        
        # 保存原始位置
        self.original_pos = self.pos()
        
        # 获取参数值
        self.shake_amplitude = self.amplitude_slider.value()
        self.shake_duration = self.duration_slider.value()
        frequency = self.frequency_slider.value()
        self.shake_mode_index = self.shake_mode.currentIndex()
        
        # 计算抖动步数和定时器间隔
        total_steps = int(self.shake_duration * frequency)
        self.max_shake_steps = min(total_steps, 200)  # 限制最大步数，防止卡顿
        self.shake_steps = 0
        
        # 设置定时器间隔
        interval = 1000 // frequency  # 毫秒
        self.shake_timer.start(interval)
        
        # 重置进度条
        self.progress_bar.setValue(0)
        
        # 更新抖动次数
        self.shake_count += 1
        self.count_label.setText(f'抖动次数: {self.shake_count}')
        
        # 重置最大偏移记录
        self.max_offset = 0
        
    def shake_step(self):
        """执行一次抖动步骤"""
        if self.shake_steps >= self.max_shake_steps:
            self.stop_shake()
            return
            
        # 计算当前进度
        progress = self.shake_steps / self.max_shake_steps
        
        # 使用阻尼效果，使抖动幅度逐渐减小
        damping = 1.0 - progress * 0.7  # 保留30%的振幅到最后
        
        # 根据选择的模式计算偏移
        mode = self.shake_mode_index
        
        if mode == 0:  # 随机抖动
            x_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * damping
            y_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * damping
        elif mode == 1:  # 水平抖动
            x_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * damping
            y_offset = 0
        elif mode == 2:  # 垂直抖动
            x_offset = 0
            y_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * damping
        elif mode == 3:  # 圆形抖动
            angle = self.shake_steps * 0.5  # 控制旋转速度
            radius = self.shake_amplitude * damping
            x_offset = radius * math.cos(angle)
            y_offset = radius * math.sin(angle)
        else:  # 地震模式
            # 模拟地震的随机强烈抖动
            if random.random() < 0.7:  # 70%概率小抖动
                x_offset = random.randint(-self.shake_amplitude//2, self.shake_amplitude//2) * damping
                y_offset = random.randint(-self.shake_amplitude//2, self.shake_amplitude//2) * damping
            else:  # 30%概率强烈抖动
                x_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * (damping + 0.5)
                y_offset = random.randint(-self.shake_amplitude, self.shake_amplitude) * (damping + 0.5)
        
        # 应用偏移
        new_x = self.original_pos.x() + x_offset
        new_y = self.original_pos.y() + y_offset
        self.move(int(new_x), int(new_y))
        
        # 更新最大偏移记录
        current_offset = math.sqrt(x_offset**2 + y_offset**2)
        if current_offset > self.max_offset:
            self.max_offset = int(current_offset)
            self.max_offset_label.setText(f'最大偏移: {self.max_offset} 像素')
        
        # 更新进度条
        self.progress_bar.setValue(int(progress * 100))
        
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
        self.stop_button.setEnabled(False)
        self.shake_button.setText('🚀 开始抖动窗口')
        self.status_label.setText('窗口状态: 正常')
        self.status_label.setStyleSheet('font-size: 16px; margin: 10px; padding: 10px; background-color: #E8F5E9; border-radius: 5px; color: #4CAF50;')
        
        # 更新总抖动时间
        self.total_shake_time += self.shake_duration
        self.total_time_label.setText(f'总抖动时间: {self.total_shake_time} 秒')
        
        # 重置进度条
        self.progress_bar.setValue(100)
        
        # 短暂显示完成状态
        QTimer.singleShot(1000, lambda: self.progress_bar.setValue(0))
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.is_shaking:
            self.shake_timer.stop()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    # 设置应用图标和样式
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 248, 255))
    palette.setColor(QPalette.WindowText, QColor(33, 33, 33))
    app.setPalette(palette)
    
    # 创建并显示窗口
    window = ShakeWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()