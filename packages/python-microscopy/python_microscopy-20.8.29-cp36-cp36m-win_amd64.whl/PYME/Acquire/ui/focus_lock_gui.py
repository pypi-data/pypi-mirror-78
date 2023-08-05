
import wx

class FocusLockPanel(wx.Panel):
    def __init__(self, parent, focus_PID, winid=-1, offset_piezo=None):
        """
        Parameters
        ----------
        offset_piezo : PYME.Acquire.Hardware.Piezos.offsetPiezoREST.OffsetPiezo
            offset piezo; only used to display current offset
        """
        wx.Panel.__init__(self, parent, winid)
        self.servo = focus_PID
        self.offset_piezo = offset_piezo

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        self.lock_checkbox = wx.CheckBox(self, -1, 'Lock')
        self.lock_checkbox.Bind(wx.EVT_CHECKBOX, self.OnToggleLock)
        hsizer.Add(self.lock_checkbox, 0, wx.ALL, 2)

        self.set_position_button = wx.Button(self, -1, 'Set Focus')
        hsizer.Add(self.set_position_button, 0, wx.ALL, 2)
        self.set_position_button.Bind(wx.EVT_BUTTON, self.OnUpdateSetpoint)

        self.set_subtraction_button = wx.Button(self, -1, 'Set Dark')
        hsizer.Add(self.set_subtraction_button, 0, wx.ALL, 2)
        self.set_subtraction_button.Bind(wx.EVT_BUTTON, self.OnSetSubtractionProfile)

        sizer_1.Add(hsizer, 0, wx.EXPAND, 0)

        if self.offset_piezo is not None:
            offset, offset_range = self._get_offset_and_range()

            self._offset_slider = wx.Slider(self, -1, 100 * (offset - offset_range[0]), 
                                           0, 
                                           100 * (offset_range[1] - offset_range[0]), 
                                           size=wx.Size(100, -1),
                                           style=wx.SL_HORIZONTAL)
            self._offset_label = wx.StaticBox(self, -1, u'%s: %2.3f %s' % ('offset', offset, u'\u03BCm'))
            
            hsizer = wx.StaticBoxSizer(self._offset_label, wx.HORIZONTAL)
            hsizer.Add(self._offset_slider, 1, wx.ALL|wx.EXPAND, 0)
            sizer_1.Add(hsizer, 0, wx.EXPAND, 0)

        self.SetSizerAndFit(sizer_1)
    
    def _get_offset_and_range(self):
        target = self.offset_piezo.GetTargetPos()
        offset = self.offset_piezo.GetOffset()
        min_pos, max_pos = self.offset_piezo.GetMin(), self.offset_piezo.GetMax()
        #  basePiezo position - offset = OffsetPiezo position
        min_offset = -(target + min_pos)
        max_offset = max_pos - target

        return offset, (min_offset, max_offset)

    def OnToggleLock(self, event):
        self.servo.ToggleLock()

    def OnUpdateSetpoint(self, event):
        self.servo.ChangeSetpoint()

    def OnSetSubtractionProfile(self, event):
        self.servo.SetSubtractionProfile()

    def refresh(self):
        self.lock_checkbox.SetValue(bool(self.servo.lock_enabled))
        if self.offset_piezo is not None:
            offset, offset_range = self._get_offset_and_range()

            self._offset_slider.SetValue(int(100 * (offset - offset_range[0])))
            self._offset_slider.SetMin(0)
            self._offset_slider.SetMax(100 * (offset_range[1] - offset_range[0]))
            self._offset_label.SetLabel(u'%s: %2.3f %s' % ('offset', offset, u'\u03BCm'))
