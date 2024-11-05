import tkinter as tk
import wx

def create_selection_dialog(title, options):
    selected_value = []

    def show_selection():
        selected_value.append(variable.get())
        root.quit()

    root = tk.Tk()
    root.geometry("300x200")
    root.resizable(0, 0)
    root.title(title)
    variable = tk.StringVar(root)
    variable.set(options[0])
    dropdown = tk.OptionMenu(root, variable, *options)
    dropdown.pack(pady=20)
    select_button = tk.Button(root, text="确定", command=show_selection)
    select_button.pack(pady=20)
    root.mainloop()
    root.destroy()

    return selected_value[0] if selected_value else None

class MultiSelectList(wx.Frame):
    def __init__(self, data, additional_data, max_members, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data = data
        self.additional_data = additional_data
        self.max_members = max_members
        self.selected_items = []

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox_left = wx.BoxSizer(wx.VERTICAL)
        vbox_right = wx.BoxSizer(wx.VERTICAL)

        self.check_list_box = wx.CheckListBox(panel, choices=[
            f"Lv. {item['level']} | {item['char_name']} | 职业：{item['jobName']} | {self.format_attributes(item)}" for item in data
        ])
        self.check_list_box.Bind(wx.EVT_CHECKLISTBOX, self.on_item_toggled)

        for i in range(len(data)): 
            self.check_list_box.Check(i)

        self.selected_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_BESTWRAP)
        self.selected_text.SetMinSize((200, -1))

        vbox_left.Add(self.check_list_box, 1, wx.EXPAND | wx.ALL, 10)
        vbox_right.Add(wx.StaticText(panel, label="角色卡属性增益"), 0, wx.EXPAND | wx.ALL, 10)
        vbox_right.Add(self.selected_text, 1, wx.EXPAND | wx.ALL, 10)

        # Adding additional checkboxes
        self.additional_checkbox1 = wx.CheckBox(panel, label="持有深渊远征队-米纳尔森林联盟积木")
        self.additional_checkbox1.Bind(wx.EVT_CHECKBOX, self.on_item_toggled)
        self.additional_checkbox2 = wx.CheckBox(panel, label="持有深渊远征队-冰峰雪域联盟积木")
        self.additional_checkbox2.Bind(wx.EVT_CHECKBOX, self.on_item_toggled)
        vbox_right.Add(self.additional_checkbox1, 0, wx.EXPAND | wx.ALL, 5)
        vbox_right.Add(self.additional_checkbox2, 0, wx.EXPAND | wx.ALL, 5)

        self.confirm_button = wx.Button(panel, label="确定")
        self.confirm_button.Enabled = False
        self.confirm_button.Bind(wx.EVT_BUTTON, self.on_confirm_selection)
        vbox_right.Add(self.confirm_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        hbox.Add(vbox_left, 1, wx.EXPAND | wx.ALL, 10)
        hbox.Add(vbox_right, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(hbox)

        self.SetSize((960, 400))
        self.SetTitle("请选择需要放入战斗地图的角色")
        self.Centre()

    def format_attributes(self, item):
        return ', '.join(f"{key}：{value}" for key, value in item.items() if key not in ["char_name", "job", "level", "jobName"])

    def on_item_toggled(self, event):
        selected_indices = self.check_list_box.GetCheckedItems()
        if len(selected_indices) <= self.max_members:
            self.confirm_button.Enabled = True
        else:
            self.confirm_button.Enabled = False
        self.selected_items = [self.data[i] for i in selected_indices]
        selected_names = [self.data[i]["char_name"] for i in selected_indices]

        # Include the additional data if checkboxes are checked
        if self.additional_checkbox1.IsChecked():
            self.selected_items.append(self.additional_data[0])
            selected_names.append(self.additional_data[0]["char_name"])
        if self.additional_checkbox2.IsChecked():
            self.selected_items.append(self.additional_data[1])
            selected_names.append(self.additional_data[1]["char_name"])

        # Calculate the sum of attributes
        summed_attributes = self.sum_attributes(self.selected_items)
        attributes_text = '\r\n'.join(f"{k}: {v}" for k, v in summed_attributes.items())

        if not self.confirm_button.Enabled:
            attributes_text = f"你选择了{len(selected_indices)}个角色，但你最多可以摆放{self.max_members}个角色\r\n\r\n" + attributes_text

        self.selected_text.SetValue(f"{attributes_text if attributes_text else ''}")
        event.Skip()

    def sum_attributes(self, items):
        summed_attributes = {}
        for item in items:
            for key, value in item.items():
                if key not in ["char_name", "job", "level", "jobName"]:
                    if key in summed_attributes:
                        summed_attributes[key] += value
                    else:
                        summed_attributes[key] = value
        return summed_attributes

    def on_confirm_selection(self, event):
        if self.additional_checkbox1.IsChecked() and self.additional_data[0] not in self.selected_items:
            self.selected_items.append(self.additional_data[0])
        if self.additional_checkbox2.IsChecked() and self.additional_data[1] not in self.selected_items:
            self.selected_items.append(self.additional_data[1])
        self.Destroy()

def create_multi_select_list(data, additional_data, max_members=99):
    app = wx.App(False)
    frame = MultiSelectList(data, additional_data, max_members, None)
    frame.Show()
    app.MainLoop()
    return frame.selected_items

additional_data = [
    {"char_name": "MinarForest", "job": 312, "level": 200, "攻击力": 16, "魔法攻击力": 16},
    {"char_name": "ElNath", "job": 512, "level": 200, "攻击力": 16, "魔法攻击力": 16}
]
