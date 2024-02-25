import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr
import maya.cmds as cmds
import os
import maya.mel as mel


def maya_useNewAPI():
    pass

#########################
### Node:  krHelpText ###
#########################
'''
Use:    Node Editor

Plugs Input:        None

Plugs Output:       None

Node Attributes:    text_display    String      The text to be displayed
                    text_coord_x    int         x position of the text
                    text_coord_r    int         y position of the text
                    colour          enum        black, white, red, green, blue, yellow, papaya, pink
'''

class HelpTextNode(omui.MPxLocatorNode):

    TYPE_NAME = "krHelpText"
    TYPE_ID = om.MTypeId(0x0007f7fb)
    DRAW_CLASSIFICATION = 'drawdb/geometry/krHelpText'
    DRAW_REGISTRANT_ID = 'HelpTextNode'

    def __init__(self):
        super(HelpTextNode, self).__init__()

    @classmethod
    def creator(cls):
        return HelpTextNode()

    @classmethod
    def initialize(cls):
        
        text_attr= om.MFnTypedAttribute()
        numeric_attr = om.MFnNumericAttribute()
        enum_attr = om.MFnEnumAttribute()
        
        
        cls.text_obj = text_attr.create('text_display', 'txt', om.MFnData.kString)
        
        cls.text_size_obj = numeric_attr.create('text_size', 'size', om.MFnNumericData.kInt, 16)
        
        cls.text_align_obj = enum_attr.create('text_align', 'align', 1)
        enum_attr.addField('Left', 0)
        enum_attr.addField('Centre', 1)
        enum_attr.addField('Right', 2)
        
        cls.text_coord_x_obj = numeric_attr.create('text_x_percentage', 'coordx', om.MFnNumericData.kInt)
        numeric_attr.keyable = True
        
        cls.text_coord_y_obj = numeric_attr.create('text_y_percentage', 'coordy', om.MFnNumericData.kInt)
        numeric_attr.keyable = True
        
        cls.x_centre_obj = numeric_attr.create('centre_x_axis', 'centrex', om.MFnNumericData.kBoolean)
        cls.y_centre_obj = numeric_attr.create('centre_y_axis', 'centrey', om.MFnNumericData.kBoolean)
        
        
        cls.text_colour_enum_obj = enum_attr.create('colour', 'col', 1)
        enum_attr.addField('black', 0)
        enum_attr.addField('white', 1)
        enum_attr.addField('red', 2)
        enum_attr.addField('green', 3)
        enum_attr.addField('blue', 4)
        enum_attr.addField('yellow', 5)
        enum_attr.addField('papaya', 6)
        enum_attr.addField('pink', 7)
        
        
        enum_attr.keyable = True
        enum_attr.hidden = False
        
        # add the attributes
        
        cls.addAttribute(cls.text_obj)
        cls.addAttribute(cls.text_size_obj)
        # cls.addAttribute(cls.text_weight_obj)
        cls.addAttribute(cls.text_align_obj)
        cls.addAttribute(cls.text_coord_x_obj)
        cls.addAttribute(cls.text_coord_y_obj)
        cls.addAttribute(cls.x_centre_obj)
        cls.addAttribute(cls.y_centre_obj)
        cls.addAttribute(cls.text_colour_enum_obj)
        

class HelpTextDrawOverride(omr.MPxDrawOverride):
    
    NAME = "HelpTextDrawOverride"
    
    def __init__(self, obj):
        super(HelpTextDrawOverride, self).__init__(obj, None, False)  
        self.text_to_display = 'Well, hello there...'
        self.text_col_r = 1
        self.text_col_g = 1
        self.text_col_b = 1
        self.text_size = 16
        self.text_align = 1
        self.text_weight = 400
        self.text_coord_x = 100
        self.text_coord_y = 100
        
    
    def prepareForDraw(self, obj_path, camera_path, frame_context, old_data):
        
        view = omui.M3dView.active3dView()
        width, height = view.portWidth(), view.portHeight()
        
        text_plug = om.MPlug(obj_path.node(), HelpTextNode.text_obj)
        text_data = text_plug.asString()
        self.text_to_display = text_data or ''
        
        size_plug = om.MPlug(obj_path.node(), HelpTextNode.text_size_obj)
        size_data = size_plug.asInt()
        self.text_size = size_data
        
        align_plug = om.MPlug(obj_path.node(), HelpTextNode.text_align_obj)
        align_data = align_plug.asInt()
        self.text_align = align_data
        
        
        c_x_plug = om.MPlug(obj_path.node(), HelpTextNode.x_centre_obj)
        c_x_data = c_x_plug.asBool()
        
        c_y_plug = om.MPlug(obj_path.node(), HelpTextNode.y_centre_obj)
        c_y_data = c_y_plug.asBool()
        
        coords_x_plug = om.MPlug(obj_path.node(), HelpTextNode.text_coord_x_obj)
        coords_x_data = coords_x_plug.asInt()
        self.text_coord_x = (width / 100) * coords_x_data
        
        
        coords_y_plug = om.MPlug(obj_path.node(), HelpTextNode.text_coord_y_obj)
        coords_y_data = coords_y_plug.asInt()
        self.text_coord_y = (height / 100) * coords_y_data
        
        if c_x_data:
            self.text_coord_x = width / 2
            
        if c_y_data:
            self.text_coord_y = height / 2
            
        
        
        
        colour_plug = om.MPlug(obj_path.node(), HelpTextNode.text_colour_enum_obj)
        colour_data = colour_plug.asInt()
        
        if colour_data == 0:
            self.text_col_r = 0
            self.text_col_g = 0
            self.text_col_b = 0
        
        if colour_data == 1:
            self.text_col_r = 1
            self.text_col_g = 1
            self.text_col_b = 1
        
        if colour_data == 2:
            self.text_col_r = 0.8
            self.text_col_g = 0
            self.text_col_b = 0
        
        if colour_data == 3:
            self.text_col_r = 0
            self.text_col_g = 0.8
            self.text_col_b = 0
        
        if colour_data == 4:
            self.text_col_r = 0
            self.text_col_g = 0
            self.text_col_b = 0.8
        
        if colour_data == 5:
            self.text_col_r = 1
            self.text_col_g = 1
            self.text_col_b = 0
        
        if colour_data == 6:
            self.text_col_r = 1
            self.text_col_g = 0.5
            self.text_col_b = 0
        
        if colour_data == 7:
            self.text_col_r = 0.5
            self.text_col_g = 0
            self.text_col_b = 1
        
        
    def supportedDrawAPIs(self):
        return omr.MRenderer.kAllDevices
        
    def hasUIDrawables(self):
        return True
    
    def addUIDrawables(self, obj_path, draw_manager, frame_context, data):
        text_colour = om.MColor((self.text_col_r, self.text_col_g, self.text_col_b, 1))
        
        
        draw_manager.beginDrawable()
        draw_manager.setColor(text_colour)
        draw_manager.setFontSize(self.text_size)
        # draw_manager.setFontWeight(self.text_weight)
        if self.text_align == 0:
            draw_manager.text2d(om.MPoint(self.text_coord_x, self.text_coord_y), self.text_to_display, omr.MUIDrawManager.kLeft)
        if self.text_align == 1:
            draw_manager.text2d(om.MPoint(self.text_coord_x, self.text_coord_y), self.text_to_display, omr.MUIDrawManager.kCenter)
        if self.text_align == 2:
            draw_manager.text2d(om.MPoint(self.text_coord_x, self.text_coord_y), self.text_to_display, omr.MUIDrawManager.kRight)
        
        draw_manager.endDrawable()
        
    @classmethod
    def creator(cls, obj):
        return HelpTextDrawOverride(obj)



##########################
### Node:  krCondition ###
##########################
'''
Use:    Node Editor

Plugs Input:        Operation   - whether Equal to, not equal to, greater than, greater than or equal to, less than, less than or equal to

Plugs Output:       Result

Node Attributes:    Value if true   - the value output if the condition is true
                    Value if false  - the value output if the value is false
                    
'''

class AttrCheckNode(om.MPxNode):

    TYPE_NAME = "krCondition"
    TYPE_ID = om.MTypeId(0x0007F7F8)
    
    term_one_obj = None
    term_two_obj = None
    value_true_obj = None
    value_false_obj = None
    operation_obj = None
    result_obj = None
    
    def __init__(self):
        super(AttrCheckNode, self).__init__()
    
    def compute(self, plug, data):
        
        # when the node is dirty
        if plug == AttrCheckNode.result_obj:
            
            # get the required values
            term_one = data.inputValue(AttrCheckNode.term_one_obj).asDouble()
            term_two = data.inputValue(AttrCheckNode.term_two_obj).asDouble()
            
            value_true = data.inputValue(AttrCheckNode.value_true_obj).asDouble()
            value_false = data.inputValue(AttrCheckNode.value_false_obj).asDouble()
            
            operation = data.inputValue(AttrCheckNode.operation_obj).asInt()
            
            # set the result value
            
            result = 0.0
            
            if operation == 0:
                if term_one == term_two:
                    result = value_true
                else:
                    result = value_false
                    
            if operation == 1:
                if term_one != term_two:
                    result = value_true
                else:
                    result = value_false
                    
            if operation == 2:
                if term_one > term_two:
                    result = value_true
                else:
                    result = value_false
                    
            if operation == 3:
                if term_one >= term_two:
                    result = value_true
                else:
                    result = value_false
                    
            if operation == 4:
                if term_one < term_two:
                    result = value_true
                else:
                    result = value_false
                    
            if operation == 5:
                if term_one <= term_two:
                    result = value_true
                else:
                    result = value_false
                    
            
            output_data = data.outputValue(AttrCheckNode.result_obj)
            output_data.setDouble(result)

            
    @classmethod
    def creator(cls):
        return AttrCheckNode()
        
    @classmethod
    def initialize(cls):
    
        numeric_attr = om.MFnNumericAttribute()
        enum_attr = om.MFnEnumAttribute()
        
        # term one        
        cls.term_one_obj = numeric_attr.create('term_one', 'one', om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False
        
        # term two
        cls.term_two_obj = numeric_attr.create('term_two', 'two', om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False
        
        # value if true
        cls.value_true_obj = numeric_attr.create('value_true', 'true', om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False        

        # value if false
        cls.value_false_obj = numeric_attr.create('value_false', 'false', om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False

        # operation enum
        cls.operation_obj = enum_attr.create('operation', 'op', 0)
        enum_attr.keyable = True
        enum_attr.readable = False
        
        enum_attr.addField('equal', 0)
        enum_attr.addField('not equal', 1)
        enum_attr.addField('greater than', 2)
        enum_attr.addField('greater then or equal', 3)
        enum_attr.addField('less than', 4)
        enum_attr.addField('less than or equal', 5)
        
        # output node
        cls.result_obj = numeric_attr.create('result', 'res', om.MFnNumericData.kDouble, 0.0)
        numeric_attr.writable = False
        
        # add attributes
        cls.addAttribute(cls.term_one_obj)
        cls.addAttribute(cls.operation_obj)
        cls.addAttribute(cls.term_two_obj)
        cls.addAttribute(cls.value_true_obj)
        cls.addAttribute(cls.value_false_obj)
        cls.addAttribute(cls.result_obj)     
        
        # affects
        cls.attributeAffects(cls.term_one_obj, cls.result_obj)
        cls.attributeAffects(cls.term_two_obj, cls.result_obj)
        cls.attributeAffects(cls.value_true_obj, cls.result_obj)
        cls.attributeAffects(cls.value_false_obj, cls.result_obj)
        cls.attributeAffects(cls.operation_obj, cls.result_obj)
        
    
##########################################
### Basic Node:  krMultiEqualCondition ###
##########################################
'''
Use:    Node Editor

Plugs Input:        Input

Plugs Output:       Output

Node Attributes:    Check 00 to Check 09
                    First:  the number to check
                    Second: the output if a match
                    
'''

class ConvertInputNode(om.MPxNode):

    TYPE_NAME = "krMultiEqualCondition"
    TYPE_ID = om.MTypeId(0x0007F7F7)
    
    input_obj = None
    output_obj = None
    
    def __init__(self):
        super(ConvertInputNode, self).__init__()
    
    def compute(self, plug, data):
        # when the node is dirty
        if plug == ConvertInputNode.output_obj:
            
            # set the initial output var - if no match, 0.0 will be the output
            my_output = 0.0
            
            # get the input variable
            my_input = data.inputValue(ConvertInputNode.input_obj).asDouble()
            
            # used to stop checking incase of duplicates - will stop when the first match is found.
            match_found = False

            for index in range(10):
                if not match_found:
                    # get the data
                    check_attr_name = f"check_0{str(index)}"
                    my_check_data = data.inputValue(getattr(ConvertInputNode, check_attr_name)).asDouble2()
                    my_check = my_check_data[0]
                    my_result = my_check_data[1]
                    
                    # check the data
                    if my_input == my_check:
                        my_output = my_result
                        match_found = True
            
            # set the outputs        
            output_data_handle = data.outputValue(ConvertInputNode.output_obj)
            output_data_handle.setDouble(my_output)
        
    @classmethod
    def creator(cls):
        return ConvertInputNode()
        
    @classmethod
    def initialize(cls):
    
        numeric_attr = om.MFnNumericAttribute()
        
        # input node
        cls.input_obj = numeric_attr.create('input', 'inp', om.MFnNumericData.kDouble, 0.0)
        numeric_attr.keyable = True
        numeric_attr.readable = False
        
        # output node
        cls.output_obj = numeric_attr.create('output', 'out', om.MFnNumericData.kDouble, 0.0)
        numeric_attr.writable = False
        
        # add attributes
        cls.addAttribute(cls.input_obj)
        cls.addAttribute(cls.output_obj)        
        
        for index in range(10):
            index_str = str(index)
            exec(f"cls.check_0{index_str} = numeric_attr.create('check_0{index_str}', 'ch0{index_str}', om.MFnNumericData.k2Double, index)")
            exec(f'cls.addAttribute(cls.check_0{index_str})')
            exec(f'cls.attributeAffects(cls.check_0{index_str}, cls.output_obj)')
            
        # affects
        cls.attributeAffects(cls.input_obj, cls.output_obj)
     
        pass
        
    
##################################
### Context Command:  krSelect ###
##################################
'''
use:    From Python:    cmds.krSelect(attribute = 'attr_name')
        Can be added to the toolbar if required, but no real purpose will result from that

Flags:          mesh = True     select meshes only
                joint = True    select joints only
        
Flag args:      attribute = 'attr_name'     MANDATORY   string ~ name of the attribute to be added to the selection
                number = 2                  Optional    maximum number of items to be selected.  Unlimited if not used

###  ADDED:   text = 'test1|test2|Press Enter'
    
    should only be used when there is a specific number.  Do the amount of options, plus one final one to tell the user to press enter
    
###

'''

class SelectObjectContext(omui.MPxContext):
    
    TITLE = 'Select Object Context'

    def __init__(self):
        super(SelectObjectContext, self).__init__()
        
        prefs_dir = os.getenv('MAYA_APP_DIR')
        image_path = f'{prefs_dir}/prefs/icons/kr_select.png'
        
        self.setTitleString(SelectObjectContext.TITLE)
        self.setImage(image_path, omui.MPxContext.kImage1)
        
        self.state = 0
        self.context_selection = om.MSelectionList()
        
        # true when the flag is used
        self.set_mesh = False
        self.set_joint = False
        self.set_curve = False
        self.set_number = False
        
        
        self.set_attr = False
    
        # set the number of selection and the attribute attributes
        self.number = None
        self.attr = None
        
        self.my_selection = []
        
        obj = 'krHelpText001'
        if cmds.objExists(obj):
            par = cmds.listRelatives(obj, parent = True)
            if par:
                cmds.delete(par)
            else:
                cmds.delete(obj)
        self.my_help = cmds.createNode('krHelpText', name = obj)
        par = cmds.listRelatives(self.my_help, parent = True)
        if par:
            cmds.rename(par, 'krHelpText_001')
        
        
        self.help_text = 'Test'
        self.help2 = None
        
        
        

    def toolOnSetup(self, event):
        om.MGlobal.selectCommand(om.MSelectionList())
        self.reset_state()
        self.update_help()
        
    def toolOffCleanup(self):
        mel.eval('setObjectPickMask "Joint" true')
        mel.eval('setObjectPickMask "Curve" true')
        mel.eval('setObjectPickMask "Surface" true')
        mel.eval('setObjectPickMask "Deformer" true')
        mel.eval('setObjectPickMask "Dynamic" true')
        mel.eval('setObjectPickMask "Rendering" true')    
        self.reset_state()
        self.help_text = ''
        cmds.setAttr(self.my_help + '.text_display', self.help_text, type = 'string')
        
        
    def doRelease(self, event, draw_manager, frame_context):
        # create the select mask variable
        select_mask = None
        
        # if joints - set the mask to joints
        if self.set_joint:
            select_mask = om.MSelectionMask.kSelectJoints
        
        # else set the mask to meshes
        else:
            select_mask = om.MSelectionMask.kSelectMeshes
        
        # selection if a number is passed
        if self.number:
            if self.state >=0 and self.state < self.number:    
                om.MGlobal.selectFromScreen(event.position[0], event.position[1], 
                                            event.position[1], event.position[1], 
                                            om.MGlobal.kReplaceList, select_mask)
        
        # selection if there is no number
        else:
            om.MGlobal.selectFromScreen(event.position[0], event.position[1], 
                            event.position[1], event.position[1], 
                            om.MGlobal.kReplaceList, select_mask)

        active_selection = om.MGlobal.getActiveSelectionList()

        for index in reversed(range(active_selection.length())):
            obj = active_selection.getDependNode(index)
            select_type = obj.apiType()
            
            if self.set_mesh and select_type != 110:
                active_selection.remove(index)
                
            elif self.set_joint and select_type != 121:
                active_selection.remove(index)
                
            elif select_type != 110 and select_type != 121:
                active_selection.remove(index)
            
            
            
        if active_selection.length() == 1:
            self.context_selection.merge(active_selection)
            
        om.MGlobal.setActiveSelectionList(self.context_selection)
        
        self.update_state()
            
    def completeAction(self):
        # create the selection list
        selection_count = self.context_selection.length()
        self.selection_list = []
        
        
        if selection_count > 0:
            # clear the om.selection list
            om.MGlobal.setActiveSelectionList(om.MSelectionList())
            
            for index in range(selection_count):
                transform_fn = om.MFnTransform(self.context_selection.getDependNode(index))
                
                # get the name of the selection item
                name = transform_fn.name()
                
                # add it to the selection list
                self.selection_list.append(name)
                
        # if the attribute is passed
        if self.attr:
            # clear the attribute if set on any item in the scene
            
            # get all items in the scene
            all_items = cmds.ls()
            
            # get the attr argument
            long_name = self.attr
            
            # iterate through the scene, and check for anything that already has the attribute.
            for item in all_items:
                if cmds.attributeQuery(long_name, node = item, exists = True):
                    
                    # if the item has the attribute, then delete it
                    cmds.deleteAttr(item, attribute = long_name)
            
            # iterate through the selection, then add the attribute to the selected items
            count = 1
            for item in self.selection_list:
                if self.help2:
                    my_attr = cmds.addAttr(item, longName = f'{long_name}_{count}', attributeType = 'bool', keyable = False)
                    cmds.setAttr(f'{item}.{self.attr}_{count}', True)
                else:
                    my_attr = cmds.addAttr(item, longName = long_name, attributeType = 'bool', keyable = False)
                    cmds.setAttr(f'{item}.{self.attr}', True)
                count += 1
             
        mel.eval('setObjectPickMask "Joint" true')
        mel.eval('setObjectPickMask "Curve" true')
        mel.eval('setObjectPickMask "Surface" true')
        mel.eval('setObjectPickMask "Deformer" true')
        mel.eval('setObjectPickMask "Dynamic" true')
        mel.eval('setObjectPickMask "Rendering" true')       
        
        self.reset_state()
        self.help_text = ''
        cmds.setAttr(self.my_help + '.text_display', self.help_text, type = 'string')
        # superContext to return to the standard selection tool
        cmds.setToolTo('selectSuperContext')
        
    def deleteAction(self):
        # remove the last item from the list
        selection_count = self.context_selection.length()
        
        # if there is a selection, remove the last item selected
        if selection_count > 0:
            self.context_selection.remove(selection_count -1)
            
            om.MGlobal.setActiveSelectionList(self.context_selection)
            
            self.update_state()
        
    def abortAction(self):
        # if the escape is pressed, reset the tool and go back to the main selection tool
        self.reset_state()
        cmds.setToolTo('selectSuperContext')
        
    def update_state(self):
        # update the state variable with the length of the selection
        self.state = self.context_selection.length()
        self.update_help()
        
    def reset_state(self):
        # clear the selection
        om.MGlobal.setActiveSelectionList(om.MSelectionList())
        self.context_selection.clear()
        self.update_state()
        
    def update_help(self):
        # update the help text
        item = 'meshes'
        if self.number == 1 and self.set_mesh:
            item = 'mesh'
        elif self.number == 1 and self.set_joint:
            item = 'joint'
        elif self.set_mesh:
            item = 'meshes'
        elif self.set_joint:
            item = 'joints'
        
        cmds.setAttr(self.my_help + '.text_display', f'Select the {item}, then press Enter.  *press Backspace to deselect of Esc to cancel', type = 'string')
        
        if self.help2:
            
            cmds.setAttr(self.my_help + '.text_display', self.help2[self.state], type = 'string')
            pass
        
        
class SelectObjectContextCmd(omui.MPxContextCommand):
    COMMAND_NAME = 'krSelect'
    
    # flags
    MESH_FLAG = ['-m', '-mesh']
    JOINT_FLAG = ['-j', '-joint']
    NUMBER_FLAG = ['-n', '-number']
    ATTR_FLAG = ['-a', '-attribute']
    HELP_FLAG = ['-h', '-help']
    TXT_FLAG = ['-t', '-text']
    
    def __init__(self):
        super(SelectObjectContextCmd, self).__init__()


        
    def makeObj(self):
        self.my_context = SelectObjectContext()
        return self.my_context
        
    def appendSyntax(self):
        # get the current syntax
        my_syntax = self.syntax()
        
        # add the flags
        my_syntax.addFlag(SelectObjectContextCmd.MESH_FLAG[0], 
                          SelectObjectContextCmd.MESH_FLAG[1])
        my_syntax.addFlag(SelectObjectContextCmd.JOINT_FLAG[0], 
                          SelectObjectContextCmd.JOINT_FLAG[1])
        my_syntax.addFlag(SelectObjectContextCmd.HELP_FLAG[0], 
                          SelectObjectContextCmd.HELP_FLAG[1])
        
        # add the flags with arguments
        my_syntax.addFlag(SelectObjectContextCmd.NUMBER_FLAG[0], 
                          SelectObjectContextCmd.NUMBER_FLAG[1], om.MSyntax.kUnsigned)        
        my_syntax.addFlag(SelectObjectContextCmd.ATTR_FLAG[0], 
                          SelectObjectContextCmd.ATTR_FLAG[1], om.MSyntax.kString)     
                          
        my_syntax.addFlag(SelectObjectContextCmd.TXT_FLAG[0], 
                          SelectObjectContextCmd.TXT_FLAG[1], om.MSyntax.kString)     
                          
        
        
    def doEditFlags(self):
        # get the args list
        args = self.parser()
        
        # define the number variable
        number = None
        
        # check for mesh flag
        if args.isFlagSet('-m'):
            self.my_context.set_mesh = True
            mel.eval('setObjectPickMask "Joint" false')
            mel.eval('setObjectPickMask "Curve" false')
            mel.eval('setObjectPickMask "Surface" true')
            mel.eval('setObjectPickMask "Deformer" false')
            mel.eval('setObjectPickMask "Dynamic" false')
            mel.eval('setObjectPickMask "Rendering" false')           

        # check for joint flag
        if args.isFlagSet('-j'):
            self.my_context.set_joint = True
            mel.eval('setObjectPickMask "Joint" true')
            mel.eval('setObjectPickMask "Curve" false')
            mel.eval('setObjectPickMask "Surface" false')
            mel.eval('setObjectPickMask "Deformer" false')
            mel.eval('setObjectPickMask "Dynamic" false')
            mel.eval('setObjectPickMask "Rendering" false')       
            

        
        # help flag
        if args.isFlagSet('-h'):
            om.MGlobal.displayInfo("Flags:  attr = 'attr_name'  ** mandatory flag ** to specify the name of the attribute to be set for the selection")
            om.MGlobal.displayInfo("Flags:  mesh = True         for a mesh selection")
            om.MGlobal.displayInfo("Flags:  joint = True        for a mesh selection")
            om.MGlobal.displayInfo("Flags:  number = 3          to specify the maximum number of selections")
            
        # check for number flag    
        if args.isFlagSet('-n'):
            number = args.flagArgumentInt(SelectObjectContextCmd.NUMBER_FLAG[0], 0)
            
            # update the number variable in the context class
            self.my_context.number = number
            
        if args.isFlagSet('-t'):
            txt = args.flagArgumentString(SelectObjectContextCmd.TXT_FLAG[0], 0)
            self.my_context.help2 = txt.split('|')
        
        # check if there is an attribute set.  If not, display a warning
        if not args.isFlagSet('-a'):
            om.MGlobal.displayWarning('Please set the attribute argument.')
            
        else:
            # get the attribute argument
            attr = args.flagArgumentString(SelectObjectContextCmd.ATTR_FLAG[0], 0)
            
            # set the argument in the context
            self.my_context.attr = attr
            
        # update the help text
        item = 'meshes'
        if number == 1 and self.my_context.set_mesh:
            item = 'mesh'
        elif number == 1 and self.my_context.set_joint:
            item = 'joint'
        elif self.my_context.set_mesh:
            item = 'meshes'
        elif self.my_context.set_joint:
            item = 'joints'

        self.my_context.setHelpString(f'Please select the required {item}, then press Enter.  Please press backspace to remove the selection, or Esc to cancel.')

        cmds.setAttr(self.my_context.my_help + '.centre_x_axis', 1)
        cmds.setAttr(self.my_context.my_help + '.text_y_percentage', 10)
        cmds.setAttr(self.my_context.my_help + '.text_size', 16)
        
        cmds.setAttr(self.my_context.my_help + '.colour', 6)
        
        self.my_context.update_help()
        
        
    @classmethod
    def creator(cls):
        return SelectObjectContextCmd()


#############################
### Command: krTxToOffset ###
#############################
'''
Purpose:    Transfer the existing transform attributes to the offset parent matrix
            If selection is a joint, then the joint orient will also be transferred and cleared

use:    From Python:    cmds.krTxToOffset()
        Toolbar:        script can be saved to the toolbar, then will act on the selection - one or more items can be selected

Flags:  reverse = True  Transfer the offset parent matrix back to the transform attributes
        
Args:   name of object      The name of the object to action
        []                  List of objects to action
        

                number = 2                  Optional    maximum number of items to be selected.  Unlimited if not used
'''

class TransferToOffset(om.MPxCommand):

    # define the command name
    COMMAND_NAME = "krTxToOffset"

    # define the flag names
    VERSION_FLAG = ['-v', '-version']
    REVERSE_FLAG = ['-r', '-reverse']

    def __init__(self):
        super(TransferToOffset, self).__init__()
        self.undoable = True

    def doIt(self, arg_list):
        # create the arg database (from the syntax object) - try except incase of failure
        try:
            arg_db = om.MArgDatabase(self.syntax(), arg_list)
        except:
            self.displayError('Error parsing arguments')
            raise
        
        # check whether the flags were used
        self.reverse_flag_enabled = arg_db.isFlagSet(TransferToOffset.REVERSE_FLAG[0])
        self.version_flag_enabled = arg_db.isFlagSet(TransferToOffset.VERSION_FLAG[0])
        
        # get the selection
        selection_list = arg_db.getObjectList()

        self.my_selection = []
        
        # make a list of the object names, current world space matrix and offset parent matrix (for use in the undo)
        for i in range(selection_list.length()):
            depend_fn = om.MFnDependencyNode(selection_list.getDependNode(i))
            obj_name = depend_fn.name()
            obj_type = cmds.nodeType(obj_name)
            if obj_type == 'transform' or obj_type == 'joint':
                self.my_selection.append(obj_name)
            else:
                self.displayWarning('{0} cannot be processed as it is not a transform or joint node.'.format(obj_name))
            
        # version flag to test 2 flags
        if self.version_flag_enabled:
            self.setResult('1.0.0')
            
        if self.my_selection == []:
            self.displayWarning('At least one object selection is required.  Please either select a valid object or pass in as an attribute')
        else:
            # set the initial state of all objects, including their current offset parent matrices
            for obj in self.my_selection:
                if self.reverse_flag_enabled:
                    self.fm_offset(obj)
                else:
                    self.to_offset(obj)
        
    def to_offset(self, obj_name):
        # get the current offset parent matrix
        current_offset = cmds.getAttr(obj_name + '.offsetParentMatrix')
        
        # get the object type
        obj_type = cmds.nodeType(obj_name)
        
        # check if there is an offset parent matrix, and if so, reverse it using the reverse function
        if current_offset != [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0]:
            self.fm_offset(obj_name)
        
        # get the current local space matrix
        current_xform = cmds.xform(obj_name, query = True, matrix = True)
        
        # copy the world space matrix to the offsetParentMatrix
        cmds.setAttr(obj_name + '.offsetParentMatrix', current_xform, type = 'matrix')
        
        # reset all of the transform attributes to zero - cancelling out the offset parent matrix
        cmds.move(0, 0, 0, obj_name, localSpace = True)  # ls is local space
        cmds.rotate(0, 0, 0, obj_name)
        cmds.scale(1, 1, 1, obj_name)
        cmds.setAttr(obj_name + '.shear', 0, 0, 0)     
        
        # if a joint, zero the joint orient
        if obj_type == 'joint':
            cmds.setAttr(obj_name + '.jointOrient', 0, 0, 0)

    def fm_offset(self, obj_name):
        # get the object type
        obj_type = cmds.nodeType(obj_name)
        
        # get the name of the parent
        obj_parent = cmds.listRelatives(obj_name, parent = True)
        
        # if the object has a parent, move the object to the world parent
        if obj_parent is not None:
            cmds.parent(obj_name, world = True)
        
        # get the world space for the object
        obj_xform = cmds.xform(obj_name, query = True, matrix = True, worldSpace = True)
        
        # convert the xform to an MMatrix object
        obj_matrix = om.MMatrix(obj_xform)
        
        # convert the MMatrix object to a matrix
        obj_transform_matrix = om.MTransformationMatrix(obj_matrix)
        
        # get the rotation, translation, scale and shear values
        rot = obj_transform_matrix.rotation()
        trn = obj_transform_matrix.translation(1)
        scl = obj_transform_matrix.scale(1)
        shr = obj_transform_matrix.shear(1)
        
        # transfer the rotation radians to degrees
        rot_x = om.MAngle(rot.x).asDegrees()
        rot_y = om.MAngle(rot.y).asDegrees()
        rot_z = om.MAngle(rot.z).asDegrees()

        # set the translate
        cmds.move(trn[0], trn[1], trn[2], obj_name, localSpace = True)       
        cmds.rotate(rot_x, rot_y, rot_z, obj_name)
        cmds.scale(scl[0], scl[1], scl[2], obj_name)
        cmds.setAttr(obj_name + '.shear', shr[0], shr[1], shr[2])

        # reset the offsetParentMatrix
        cmds.setAttr(obj_name + '.offsetParentMatrix', [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0], type = 'matrix')

        # reparent the object if required
        if obj_parent is not None:
            cmds.parent(obj_name, obj_parent)
            

    @classmethod
    def creator(cls):
        return TransferToOffset()
        
    @classmethod
    def create_syntax(cls):
        # create the syntax
        syntax = om.MSyntax()
        
        # set the type, and if no attributes are passed, to use the current selection
        syntax.setObjectType(om.MSyntax.kSelectionList, 0, None)
        syntax.useSelectionAsDefault(True)

        # add the flag
        syntax.addFlag(TransferToOffset.REVERSE_FLAG[0], TransferToOffset.REVERSE_FLAG[1])
        syntax.addFlag(TransferToOffset.VERSION_FLAG[0], TransferToOffset.VERSION_FLAG[1])
        
        return syntax


def initializePlugin(plugin):
    vendor = "Kimberly Randall"
    version = "1.0.0"

    plugin_fn = om.MFnPlugin(plugin, vendor, version)
    
    # krHelpText node
    try:
        plugin_fn.registerNode(HelpTextNode.TYPE_NAME,
							   HelpTextNode.TYPE_ID,
                               HelpTextNode.creator,
                               HelpTextNode.initialize,
                               om.MPxNode.kLocatorNode,
                               HelpTextNode.DRAW_CLASSIFICATION)
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(HelpTextNode.TYPE_NAME))
        
    try:
        omr.MDrawRegistry.registerDrawOverrideCreator(HelpTextNode.DRAW_CLASSIFICATION, 
                                                      HelpTextNode.DRAW_REGISTRANT_ID,
                                                      HelpTextDrawOverride.creator)
    except:
        om.MGlobal.displayError("Failed to register draw override: {0}".format(HelpTextDrawOverride.NAME))
        
    # krCondition node
    try:
        plugin_fn.registerNode(AttrCheckNode.TYPE_NAME, 
                               AttrCheckNode.TYPE_ID,
                               AttrCheckNode.creator, 
                               AttrCheckNode.initialize, 
                               om.MPxNode.kDependNode
                               )
                               
    except:
        om.MGlobal.displayError('Failed to register node:  {0}'.format(AttrCheckNode.TYPE_NAME))
    
    # krMultiEqualCondition node
    try:
        plugin_fn.registerNode(ConvertInputNode.TYPE_NAME, 
                               ConvertInputNode.TYPE_ID,
                               ConvertInputNode.creator, 
                               ConvertInputNode.initialize, 
                               om.MPxNode.kDependNode
                               )
    except:
        om.MGlobal.displayError('Failed to register node:  {0}'.format(ConvertInputNode.TYPE_NAME))

    # krSelect command
    try:
        plugin_fn.registerContextCommand(SelectObjectContextCmd.COMMAND_NAME, SelectObjectContextCmd.creator)
    except:
        om.MGlobal.displayError('Failed to register context command: {0}'. format(SelectObjectContextCmd.COMMAND_NAME))
    
    # krTxToOffset command
    try:
        plugin_fn.registerCommand(TransferToOffset.COMMAND_NAME, TransferToOffset.creator, TransferToOffset.create_syntax)
    except:
        om.MGlobal.displayError("Failed to register command: {0}".format(TransferToOffset.COMMAND_NAME))
        
def uninitializePlugin(plugin):
    plugin_fn = om.MFnPlugin(plugin)
    
    # krTxToOffset command
    try:
        plugin_fn.deregisterCommand(TransferToOffset.COMMAND_NAME)
    except:
        om.MGlobal.displayError("Failed to deregister command: {0}".format(TransferToOffset.COMMAND_NAME))
    
    
    # krSelect command
    try:
        plugin_fn.deregisterContextCommand(SelectObjectContextCmd.COMMAND_NAME)
    except:
        om.MGlobal.displayError('Failed to deregister context command: {0}'. format(SelectObjectContextCmd.COMMAND_NAME))

    # krMultiEqualCondition node
    try:
        plugin_fn.deregisterNode(ConvertInputNode.TYPE_ID)
    except:
        om.MGlobal.displayError('Failed to deregister node:  {0}'.format(ConvertInputNode.TYPE_NAME))
        
    # krCondition node
    try:
        plugin_fn.deregisterNode(AttrCheckNode.TYPE_ID)
    except:
        om.MGlobal.displayError('Failed to deregister node:  {0}'.format(AttrCheckNode.TYPE_NAME))
    
    # krHelpText node
    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator(HelpTextNode.DRAW_CLASSIFICATION, HelpTextNode.DRAW_REGISTRANT_ID)
    except:
        om.MGlobal.displayError("Failed to deregister draw override: {0}".format(HelpTextDrawOverride.NAME))
    
    try:
        plugin_fn.deregisterNode(HelpTextNode.TYPE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister node: {0}".format(HelpTextNode.TYPE_NAME))
    
