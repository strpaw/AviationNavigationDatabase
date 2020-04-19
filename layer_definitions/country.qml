<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis hasScaleBasedVisibilityFlag="0" simplifyAlgorithm="0" styleCategories="AllStyleCategories" simplifyDrawingTol="1" version="3.10.4-A Coruña" simplifyMaxScale="1" minScale="1e+08" maxScale="0" simplifyLocal="1" labelsEnabled="0" readOnly="0" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" forceraster="0" enableorderby="0" symbollevels="0">
    <symbols>
      <symbol alpha="1" type="fill" name="0" clip_to_extent="1" force_rhr="0">
        <layer class="SimpleFill" locked="0" pass="0" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="196,60,57,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="no"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option name="properties"/>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions" value="&quot;name_en&quot;"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory labelPlacementMethod="XHeight" barWidth="5" diagramOrientation="Up" scaleBasedVisibility="0" lineSizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" enabled="0" maxScaleDenominator="1e+08" penWidth="0" backgroundAlpha="255" sizeType="MM" sizeScale="3x:0,0,0,0,0,0" width="15" scaleDependency="Area" rotationOffset="270" backgroundColor="#ffffff" minScaleDenominator="0" height="15" penColor="#000000" opacity="1" penAlpha="255" minimumSize="0">
      <fontProperties style="" description="MS Shell Dlg 2,8,-1,5,50,0,0,0,0,0"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="1" obstacle="0" dist="0" linePlacementFlags="18" showAll="1" zIndex="0" priority="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration type="Map">
      <Option type="Map" name="QgsGeometryGapCheck">
        <Option type="double" name="allowedGapsBuffer" value="0"/>
        <Option type="bool" name="allowedGapsEnabled" value="false"/>
        <Option type="QString" name="allowedGapsLayer" value=""/>
      </Option>
    </checkConfiguration>
  </geometryOptions>
  <fieldConfiguration>
    <field name="rec_id">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ctry_official_name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ctry_iso3">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="ctry_short_name">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="rec_id" index="0" name=""/>
    <alias field="ctry_official_name" index="1" name=""/>
    <alias field="ctry_iso3" index="2" name=""/>
    <alias field="ctry_short_name" index="3" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default applyOnUpdate="0" field="rec_id" expression=""/>
    <default applyOnUpdate="0" field="ctry_official_name" expression=""/>
    <default applyOnUpdate="0" field="ctry_iso3" expression=""/>
    <default applyOnUpdate="0" field="ctry_short_name" expression=""/>
  </defaults>
  <constraints>
    <constraint constraints="3" field="rec_id" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint constraints="0" field="ctry_official_name" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint constraints="3" field="ctry_iso3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint constraints="0" field="ctry_short_name" exp_strength="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="rec_id" exp="" desc=""/>
    <constraint field="ctry_official_name" exp="" desc=""/>
    <constraint field="ctry_iso3" exp="" desc=""/>
    <constraint field="ctry_short_name" exp="" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortExpression="&quot;ctry_iso3&quot;" sortOrder="0">
    <columns>
      <column type="actions" hidden="1" width="-1"/>
      <column type="field" hidden="0" name="rec_id" width="-1"/>
      <column type="field" hidden="0" name="ctry_official_name" width="-1"/>
      <column type="field" hidden="0" name="ctry_iso3" width="-1"/>
      <column type="field" hidden="0" name="ctry_short_name" width="-1"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field name="ctry_iso3" editable="1"/>
    <field name="ctry_official_name" editable="1"/>
    <field name="ctry_short_name" editable="1"/>
    <field name="rec_id" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="ctry_iso3" labelOnTop="0"/>
    <field name="ctry_official_name" labelOnTop="0"/>
    <field name="ctry_short_name" labelOnTop="0"/>
    <field name="rec_id" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>"name_en"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
