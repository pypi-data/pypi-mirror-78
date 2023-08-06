/*!
 * Copyright (c) 2012 - 2020, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
*/
(function(root, factory) {
  factory(root["Bokeh"], undefined);
})(this, function(Bokeh, version) {
  var define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" && (version != null ? Bokeh[version] : Bokeh);
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh " + version + ". You have to load it prior to loading plugins.");
    }
  })
({
"ed583be1cf": /* index.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    const AwesomePanelExtensions = tslib_1.__importStar(require("f8ec988389") /* ./bokeh_extensions */);
    exports.AwesomePanelExtensions = AwesomePanelExtensions;
    const base_1 = require("@bokehjs/base");
    base_1.register_models(AwesomePanelExtensions);
},
"f8ec988389": /* bokeh_extensions\index.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    var web_component_1 = require("5c604c9068") /* ./web_component */;
    exports.WebComponent = web_component_1.WebComponent;
    var tabulator_model_1 = require("e2e34597ee") /* ./tabulator_model */;
    exports.TabulatorModel = tabulator_model_1.TabulatorModel;
    var perspective_viewer_1 = require("59f7dfa54f") /* ./perspective_viewer */;
    exports.PerspectiveViewer = perspective_viewer_1.PerspectiveViewer;
    var pivot_table_1 = require("eb1a40b8a7") /* ./pivot_table */;
    exports.PivotTable = pivot_table_1.PivotTable;
    var fast_button_1 = require("cffb3837b7") /* ./fast/fast_button */;
    exports.FastButton = fast_button_1.FastButton;
    var fast_checkbox_group_1 = require("b5be3a3047") /* ./fast/fast_checkbox_group */;
    exports.FastCheckboxGroup = fast_checkbox_group_1.FastCheckboxGroup;
},
"5c604c9068": /* bokeh_extensions\web_component.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    const dom_1 = require("@bokehjs/core/dom");
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const inputs_1 = require("@bokehjs/styles/widgets/inputs");
    function htmlDecode(input) {
        var doc = new DOMParser().parseFromString(input, "text/html");
        return doc.documentElement.textContent;
    }
    class WebComponentView extends html_box_1.HTMLBoxView {
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.name.change, () => this.handleNameChange());
            this.connect(this.model.properties.innerHTML.change, () => this.render());
            this.connect(this.model.properties.attributesLastChange.change, () => this.handleAttributesLastChangeChange());
            this.connect(this.model.properties.propertiesLastChange.change, () => this.handlePropertiesLastChangeChange());
            this.connect(this.model.properties.columnDataSource.change, () => this.handleColumnDataSourceChange());
        }
        handleNameChange() {
            if (this.label_el)
                this.label_el.textContent = this.model.name;
        }
        render() {
            super.render();
            if (this.el.innerHTML !== this.model.innerHTML)
                this.createOrUpdateWebComponentElement();
        }
        after_layout() {
            if ("after_layout" in this.webComponentElement)
                this.webComponentElement.after_layout();
        }
        createOrUpdateWebComponentElement() {
            if (this.webComponentElement)
                this.webComponentElement.onchange = null;
            // @Philippfr: How do we make sure the component is automatically sized according to the
            // parameters of the WebComponent like width, height, sizing_mode etc?
            // Should we set height and width to 100% or similar?
            // For now I've set min_height as a part of .py __init__ for some of the Wired components?
            const title = this.model.name;
            if (this.model.componentType === "inputgroup" && title) {
                this.group_el = dom_1.div({ class: inputs_1.bk_input_group }, this.label_el);
                this.group_el.innerHTML = htmlDecode(this.model.innerHTML);
                this.webComponentElement = this.group_el.firstElementChild;
                this.label_el = dom_1.label({ style: { display: title.length == 0 ? "none" : "" } }, title);
                this.group_el.insertBefore(this.label_el, this.webComponentElement);
                this.el.appendChild(this.group_el);
            }
            else {
                this.el.innerHTML = htmlDecode(this.model.innerHTML);
                this.webComponentElement = this.el.firstElementChild;
            }
            this.activate_scripts(this.webComponentElement.parentNode);
            // Initialize properties
            this.initPropertyValues();
            this.handlePropertiesLastChangeChange();
            this.handleColumnDataSourceChange();
            // Subscribe to events
            this.webComponentElement.onchange = (ev) => this.handlePropertiesChange(ev);
            this.addEventListeners();
            this.addAttributesMutationObserver();
        }
        addAttributesMutationObserver() {
            if (!this.model.attributesToWatch)
                return;
            let options = {
                childList: false,
                attributes: true,
                characterData: false,
                subtree: false,
                attributeFilter: Object.keys(this.model.attributesToWatch),
                attributeOldValue: false,
                characterDataOldValue: false
            };
            const handleAttributesChange = (_) => {
                let attributesLastChange = new Object();
                for (let attribute in this.model.attributesToWatch) {
                    const value = this.webComponentElement.getAttribute(attribute);
                    attributesLastChange[attribute] = value;
                }
                if (this.model.attributesLastChange !== attributesLastChange)
                    this.model.attributesLastChange = attributesLastChange;
            };
            let observer = new MutationObserver(handleAttributesChange);
            observer.observe(this.webComponentElement, options);
        }
        addEventListeners() {
            this.eventsCount = {};
            for (let event in this.model.eventsToWatch) {
                this.eventsCount[event] = 0;
                this.webComponentElement.addEventListener(event, (ev) => this.eventHandler(ev), false);
            }
        }
        transform_cds_to_records(cds) {
            const data = [];
            const columns = cds.columns();
            const cdsLength = cds.get_length();
            if (columns.length === 0 || cdsLength === null) {
                return [];
            }
            for (let i = 0; i < cdsLength; i++) {
                const item = {};
                for (const column of columns) {
                    let array = cds.get_array(column);
                    const shape = array[0].shape == null ? null : array[0].shape;
                    if ((shape != null) && (shape.length > 1) && (typeof shape[0] == "number"))
                        item[column] = array.slice(i * shape[1], i * shape[1] + shape[1]);
                    else
                        item[column] = array[i];
                }
                data.push(item);
            }
            return data;
        }
        // https://stackoverflow.com/questions/5999998/check-if-a-variable-is-of-function-type
        isFunction(functionToCheck) {
            if (functionToCheck) {
                const stringName = {}.toString.call(functionToCheck);
                return stringName === '[object Function]' || stringName === '[object AsyncFunction]';
            }
            else {
                return false;
            }
        }
        /**
         * Handles changes to `this.model.columnDataSource`
         * by
         * updating the data source of `this.webComponentElement`
         * using the function or property specifed in `this.model.columnDataSourceLoadFunction`
         */
        handleColumnDataSourceChange() {
            // @Philippfr: Right now we just reload all the data
            // For example Perspective has an `update` function to append data
            // Is this something we could/ should support?
            if (this.model.columnDataSource) {
                let data; // list
                const columnDataSourceOrient = this.model.columnDataSourceOrient;
                if (columnDataSourceOrient === "records")
                    data = this.transform_cds_to_records(this.model.columnDataSource);
                else
                    data = this.model.columnDataSource.data; // @ts-ignore
                const loadFunctionName = this.model.columnDataSourceLoadFunction.toString();
                const loadFunction = this.webComponentElement[loadFunctionName];
                if (this.isFunction(loadFunction))
                    this.webComponentElement[loadFunctionName](data);
                else
                    this.webComponentElement[loadFunctionName] = data;
            }
            // Todo: handle situation where this.model.columnDataSource is null
        }
        activate_scripts(el) {
            Array.from(el.querySelectorAll("script")).forEach((oldScript) => {
                const newScript = document.createElement("script");
                Array.from(oldScript.attributes)
                    .forEach(attr => newScript.setAttribute(attr.name, attr.value));
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                if (oldScript.parentNode)
                    oldScript.parentNode.replaceChild(newScript, oldScript);
            });
        }
        // See https://stackoverflow.com/questions/6491463/accessing-nested-javascript-objects-with-string-key
        /**
         * Example:
         *
         * `get_nested_property(element, "textInput.value")` returns `element.textInput.value`
         *
         * @param element
         * @param property_
         */
        get_nested_property(element, property_) {
            property_ = property_.replace(/\[(\w+)\]/g, '.$1'); // convert indexes to properties
            property_ = property_.replace(/^\./, ''); // strip a leading dot
            let a = property_.split('.');
            for (let i = 0, n = a.length; i < n; ++i) {
                let k = a[i];
                if (k in element)
                    element = element[k];
                else
                    return "";
            }
            return element;
        }
        set_nested_property(element, property_, value) {
            // @Phillipfr: I need your help to understand and solve this
            // hack: Setting the value of the WIRED-SLIDER before its ready
            // will destroy the setter.
            // I don't yet understand this.
            // if (["WIRED-SLIDER"].indexOf(element.tagName)>=0){
            //   const setter = element.__lookupSetter__(property_);
            //   if (!setter){return}
            // }
            const pList = property_.split('.');
            if (pList.length === 1)
                element[property_] = value;
            else {
                const len = pList.length;
                for (let i = 0; i < len - 1; i++) {
                    const elem = pList[i];
                    if (!element[elem])
                        element[elem] = {};
                    element = element[elem];
                }
                element[pList[len - 1]] = value;
            }
        }
        /**
         * Handles events from `eventsToWatch` by
         *
         * - Incrementing the count of the event
         * - Checking if any properties have changed
         *
         * @param ev The Event Fired
         */
        eventHandler(ev) {
            let event = ev.type;
            this.eventsCount[event] += 1;
            let eventsCountLastChanged = {};
            eventsCountLastChanged[event] = this.eventsCount[event];
            this.model.eventsCountLastChange = eventsCountLastChanged;
            this.checkIfPropertiesChanged();
        }
        /** Checks if any properties have changed. In case this is communicated to the server.
         *
         * For example the Wired `DropDown` does not run the `onchange` event handler when the selection changes.
         * Insted the `select` event is fired. Thus we can subscribe to this event and manually check for property changes.
         */
        checkIfPropertiesChanged() {
            const propertiesChange = {};
            for (const property in this.model.propertiesToWatch) {
                const oldValue = this.propertyValues[property];
                const newValue = this.get_nested_property(this.webComponentElement, property);
                if (oldValue != newValue) {
                    propertiesChange[property] = newValue;
                    this.propertyValues[property] = newValue;
                }
            }
            if (Object.keys(propertiesChange).length)
                this.model.propertiesLastChange = propertiesChange;
        }
        /** Handles the `WebComponentElement` `(on)change` event
         *
         * Communicates any changed properties in `propertiesToWatch` to the server
         * by updating `this.model.propertiesLastChange`.
         * @param ev
         */
        handlePropertiesChange(ev) {
            const properties_change = new Object();
            for (const property in this.model.propertiesToWatch) {
                if (ev.detail && property in ev.detail) {
                    properties_change[property] = ev.detail[property];
                    this.propertyValues[property] = ev.detail[property];
                }
                else if (ev.target && property in ev.target) {
                    properties_change[property] = ev.target[property];
                    this.propertyValues[property] = ev.target[property];
                }
            }
            if (Object.keys(properties_change).length)
                this.model.propertiesLastChange = properties_change;
        }
        initPropertyValues() {
            this.propertyValues = new Object();
            if (!this.webComponentElement) {
                return;
            }
            for (let property in this.model.propertiesToWatch) {
                let old_value = this.propertyValues[property];
                let new_value = this.get_nested_property(this.webComponentElement, property);
                if (new_value !== old_value) {
                    this.propertyValues[property] = new_value;
                }
            }
        }
        /**
         * Handles changes to `this.model.attributesLastChange`
         * by
         * updating the attributes of `this.webComponentElement` accordingly
         */
        handleAttributesLastChangeChange() {
            if (!this.webComponentElement)
                return;
            let attributesLastChange = this.model.attributesLastChange;
            for (let attribute in this.model.attributesLastChange) {
                if (attribute in this.model.attributesToWatch) {
                    let old_value = this.webComponentElement.getAttribute(attribute);
                    let new_value = attributesLastChange[attribute];
                    if (old_value !== new_value) {
                        if (new_value === null)
                            this.webComponentElement.removeAttribute(attribute);
                        else
                            this.webComponentElement.setAttribute(attribute, new_value);
                    }
                }
            }
        }
        /**
        * Handles changes to `this.model.propertiesLastChange`
        * by
        * updating the properties of `this.webComponentElement` accordingly
        */
        handlePropertiesLastChangeChange() {
            if (!this.webComponentElement) {
                return;
            }
            let propertiesLastChange = this.model.propertiesLastChange;
            for (let property in this.model.propertiesLastChange) {
                if (property in this.model.propertiesToWatch) {
                    let value = propertiesLastChange[property];
                    this.set_nested_property(this.webComponentElement, property, value);
                }
            }
        }
    }
    exports.WebComponentView = WebComponentView;
    WebComponentView.__name__ = "WebComponentView";
    class WebComponent extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_WebComponent() {
            this.prototype.default_view = WebComponentView;
            this.define({
                // @Philipfr: How do I make property types more specific
                componentType: [p.String, 'htmlbox'],
                innerHTML: [p.String, ''],
                attributesToWatch: [p.Any],
                attributesLastChange: [p.Any],
                propertiesToWatch: [p.Any],
                propertiesLastChange: [p.Any],
                eventsToWatch: [p.Any],
                eventsCountLastChange: [p.Any],
                columnDataSource: [p.Any],
                columnDataSourceOrient: [p.Any],
                columnDataSourceLoadFunction: [p.Any],
            });
        }
    }
    exports.WebComponent = WebComponent;
    WebComponent.__name__ = "WebComponent";
    WebComponent.__module__ = "awesome_panel_extensions.bokeh_extensions.web_component";
    WebComponent.init_WebComponent();
},
"e2e34597ee": /* bokeh_extensions\tabulator_model.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    // See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const dom_1 = require("@bokehjs/core/dom");
    // See https://docs.bokeh.org/en/latest/docs/reference/core/properties.html
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    function set_size(el, model) {
        let width_policy = model.width != null ? "fixed" : "fit";
        let height_policy = model.height != null ? "fixed" : "fit";
        const { sizing_mode } = model;
        if (sizing_mode != null) {
            if (sizing_mode == "fixed")
                width_policy = height_policy = "fixed";
            else if (sizing_mode == "stretch_both")
                width_policy = height_policy = "max";
            else if (sizing_mode == "stretch_width")
                width_policy = "max";
            else if (sizing_mode == "stretch_height")
                height_policy = "max";
            else {
                switch (sizing_mode) {
                    case "scale_width":
                        width_policy = "max";
                        height_policy = "min";
                        break;
                    case "scale_height":
                        width_policy = "min";
                        height_policy = "max";
                        break;
                    case "scale_both":
                        width_policy = "max";
                        height_policy = "max";
                        break;
                    default:
                        throw new Error("unreachable");
                }
            }
        }
        if (width_policy == "fixed" && model.width)
            el.style.width = model.width + "px";
        else if (width_policy == "max")
            el.style.width = "100%";
        if (height_policy == "fixed" && model.height)
            el.style.height = model.height + "px";
        else if (height_policy == "max")
            el.style.height = "100%";
    }
    exports.set_size = set_size;
    function transform_cds_to_records(cds) {
        const data = [];
        const columns = cds.columns();
        const cdsLength = cds.get_length();
        if (columns.length === 0 || cdsLength === null) {
            return [];
        }
        for (let i = 0; i < cdsLength; i++) {
            const item = {};
            for (const column of columns) {
                let array = cds.get_array(column);
                const shape = array[0].shape == null ? null : array[0].shape;
                if ((shape != null) && (shape.length > 1) && (typeof shape[0] == "number"))
                    item[column] = array.slice(i * shape[1], i * shape[1] + shape[1]);
                else
                    item[column] = array[i];
            }
            data.push(item);
        }
        return data;
    }
    // The view of the Bokeh extension/ HTML element
    // Here you can define how to render the model as well as react to model changes or View events.
    class TabulatorModelView extends html_box_1.HTMLBoxView {
        constructor() {
            super(...arguments);
            this._tabulator_cell_updating = false;
        }
        // objectElement: any // Element
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.properties.configuration.change, () => {
                this.render();
            });
            // this.connect(this.model.source.change, () => this.setData())
            this.connect(this.model.source.properties.data.change, () => {
                this.setData();
            });
            this.connect(this.model.source.streaming, () => this.addData());
            this.connect(this.model.source.patching, () => this.updateOrAddData());
            // this.connect(this.model.source.selected.change, () => this.updateSelection())
            this.connect(this.model.source.selected.properties.indices.change, () => this.updateSelection());
        }
        render() {
            super.render();
            console.log("render");
            const container = dom_1.div({ class: "pnx-tabulator" });
            set_size(container, this.model);
            let configuration = this.getConfiguration();
            // I'm working on getting this working in the notebook but have not yet found the solution
            // See [Issue 1529](https://github.com/holoviz/panel/issues/15299)
            if (typeof Tabulator === 'undefined') {
                // Tabulator=require("tabulator-tables")
                // requirejs(["https://unpkg.com/tabulator-tables"]);
                // Tabulator=requirejs("https://unpkg.com/tabulator-tables");
                console.log("Tabulator not loaded. See https://github.com/holoviz/panel/issues/15299");
            }
            console.log(Tabulator);
            this.tabulator = new Tabulator(container, configuration);
            this.el.appendChild(container);
        }
        getConfiguration() {
            // I refer to this via _view because this is the tabulator element when cellEdited is used
            let _view = this;
            function rowSelectionChanged(data, _) {
                console.log("rowSelectionChanged");
                let indices = data.map((row) => row.index);
                _view.model.source.selected.indices = indices;
            }
            function startUpdating() {
                _view._tabulator_cell_updating = true;
            }
            function endUpdating() {
                _view._tabulator_cell_updating = false;
            }
            function cellEdited(cell) {
                console.log("cellEdited");
                const field = cell._cell.column.field;
                const index = cell._cell.row.data.index;
                const value = cell._cell.value;
                startUpdating();
                _view.model.source.patch({ [field]: [[index, value]] });
                _view.model._cell_change = { "c": field, "i": index, "v": value };
                endUpdating();
            }
            let default_configuration = {
                "rowSelectionChanged": rowSelectionChanged,
                "cellEdited": cellEdited,
                "index": "index",
            };
            let configuration = Object.assign(Object.assign({}, this.model.configuration), default_configuration);
            let data = this.model.source;
            if (data === null || Object.keys(data.data).length === 0) {
                return configuration;
            }
            else {
                console.log("adding data to configuration");
                data = transform_cds_to_records(data);
                return Object.assign(Object.assign({}, configuration), { "data": data });
            }
        }
        after_layout() {
            console.log("after_layout");
            super.after_layout();
            this.tabulator.redraw(true);
        }
        setData() {
            console.log("setData");
            let data = transform_cds_to_records(this.model.source);
            this.tabulator.setData(data);
        }
        addData() {
            console.log("addData");
            let data = transform_cds_to_records(this.model.source);
            this.tabulator.setData(data);
        }
        updateOrAddData() {
            // To avoid double updating the tabulator data
            if (this._tabulator_cell_updating === true) {
                return;
            }
            console.log("updateData");
            let data = transform_cds_to_records(this.model.source);
            this.tabulator.setData(data);
        }
        updateSelection() {
            console.log("updateSelection");
            if (this.tabulator == null) {
                return;
            }
            let indices = this.model.source.selected.indices;
            let selectedRows = this.tabulator.getSelectedRows();
            for (let row of selectedRows) {
                if (!indices.includes(row.getData().index)) {
                    row.toggleSelect();
                }
            }
            for (let index of indices) {
                // Improve this
                // Maybe tabulator should use id as index?
                this.tabulator.selectRow(index);
            }
        }
    }
    exports.TabulatorModelView = TabulatorModelView;
    TabulatorModelView.__name__ = "TabulatorModelView";
    // The Bokeh .ts model corresponding to the Bokeh .py model
    class TabulatorModel extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_TabulatorModel() {
            this.prototype.default_view = TabulatorModelView;
            this.define({
                configuration: [p.Any,],
                source: [p.Any,],
                _cell_change: [p.Any,],
            });
        }
    }
    exports.TabulatorModel = TabulatorModel;
    TabulatorModel.__name__ = "TabulatorModel";
    TabulatorModel.__module__ = "awesome_panel_extensions.bokeh_extensions.tabulator_model";
    TabulatorModel.init_TabulatorModel();
},
"59f7dfa54f": /* bokeh_extensions\perspective_viewer.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    // Bokeh model for perspective-viewer
    // See https://github.com/finos/perspective/tree/master/packages/perspective-viewer
    // See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const dom_1 = require("@bokehjs/core/dom");
    // See https://docs.bokeh.org/en/latest/docs/reference/core/properties.html
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    const shared_1 = require("88538263fa") /* ./shared */;
    const PERSPECTIVE_VIEWER_CLASSES = [
        "perspective-viewer-material",
        "perspective-viewer-material-dark",
        "perspective-viewer-material-dense",
        "perspective-viewer-material-dense-dark",
        "perspective-viewer-vaporwave",
    ];
    function is_not_perspective_class(item) {
        return !PERSPECTIVE_VIEWER_CLASSES.includes(item);
    }
    function theme_to_class(theme) {
        return "perspective-viewer-" + theme;
    }
    // The view of the Bokeh extension/ HTML element
    // Here you can define how to render the model as well as react to model changes or View events.
    class PerspectiveViewerView extends html_box_1.HTMLBoxView {
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.source.properties.data.change, this.setData);
            this.connect(this.model.source_stream.properties.data.change, this.addData);
            this.connect(this.model.source_patch.properties.data.change, this.updateOrAddData);
            this.connect(this.model.properties.columns.change, this.updateColumns);
            this.connect(this.model.properties.parsed_computed_columns.change, this.updateParsedComputedColumns);
            this.connect(this.model.properties.computed_columns.change, this.updateComputedColumns);
            this.connect(this.model.properties.column_pivots.change, this.updateColumnPivots);
            this.connect(this.model.properties.row_pivots.change, this.updateRowPivots);
            this.connect(this.model.properties.aggregates.change, this.updateAggregates);
            this.connect(this.model.properties.filters.change, this.updateFilters);
            this.connect(this.model.properties.plugin.change, this.updatePlugin);
            this.connect(this.model.properties.theme.change, this.updateTheme);
        }
        render() {
            super.render();
            const container = dom_1.div({ class: "pnx-perspective-viewer" });
            container.innerHTML = this.getInnerHTML();
            this.perspective_element = container.children[0];
            shared_1.set_size(container, this.model);
            this.el.appendChild(container);
            this.setData();
            let viewer = this;
            function handleConfigurationChange() {
                // this refers to the perspective-viewer element
                // viewer refers to the PerspectiveViewerView element
                viewer.model.columns = this.columns; // Note columns is available as a property
                viewer.model.column_pivots = JSON.parse(this.getAttribute("column-pivots"));
                viewer.model.parsed_computed_columns = JSON.parse(this.getAttribute("parsed-computed-columns"));
                viewer.model.computed_columns = JSON.parse(this.getAttribute("computed-columns"));
                viewer.model.row_pivots = JSON.parse(this.getAttribute("row-pivots"));
                viewer.model.aggregates = JSON.parse(this.getAttribute("aggregates"));
                viewer.model.sort = JSON.parse(this.getAttribute("sort"));
                viewer.model.filters = JSON.parse(this.getAttribute("filters"));
                // Perspective uses a plugin called 'debug' once in a while.
                // We don't send this back to the python side
                // Because then we would have to include it in the list of plugins
                // the user can select from.
                const plugin = this.getAttribute("plugin");
                if (plugin !== "debug") {
                    viewer.model.plugin = this.getAttribute("plugin");
                }
            }
            this.perspective_element.addEventListener("perspective-config-update", handleConfigurationChange);
        }
        getInnerHTML() {
            let innerHTML = "<perspective-viewer style='height:100%;width:100%;'";
            innerHTML += shared_1.toAttribute("class", theme_to_class(this.model.theme));
            innerHTML += shared_1.toAttribute("columns", this.model.columns);
            innerHTML += shared_1.toAttribute("column-pivots", this.model.column_pivots);
            innerHTML += shared_1.toAttribute("computed-columns", this.model.computed_columns);
            innerHTML += shared_1.toAttribute("row-pivots", this.model.row_pivots);
            innerHTML += shared_1.toAttribute("aggregates", this.model.aggregates);
            innerHTML += shared_1.toAttribute("sort", this.model.sort);
            innerHTML += shared_1.toAttribute("filters", this.model.filters);
            innerHTML += shared_1.toAttribute("plugin", this.model.plugin);
            innerHTML += "></perspective-viewer>";
            // We don't set the parsed-computed-columns
            // It's not documented. Don't know if it is an internal thing?
            // I think it gets generated from the computed-columns currently
            // innerHTML += toAttribute("parsed-computed-columns", this.model.parsed_computed_columns)
            return innerHTML;
        }
        setData() {
            console.log("setData");
            console.log(this.model.source.data);
            let data = shared_1.transform_cds_to_records(this.model.source);
            this.perspective_element.load(data);
        }
        addData() {
            // I need to find out how to only load the streamed data
            // using this.perspective_element.update
            console.log("addData");
            this.setData();
        }
        updateOrAddData() {
            // I need to find out how to only load the patched data
            // using this.perspective_element.update
            console.log("updateOrAddData");
            this.setData();
        }
        updateAttribute(attribute, value, stringify) {
            // Might need som more testing/ a better understanding
            // I'm not sure we should return here.
            if (value === undefined || value === null || value === []) {
                return;
            }
            const old_value = this.perspective_element.getAttribute(attribute);
            if (stringify) {
                value = JSON.stringify(value);
            }
            // We should only set the attribute if the new value is different to old_value
            // Otherwise we would get a recoursion/ stack overflow error
            if (old_value !== value) {
                this.perspective_element.setAttribute(attribute, value);
            }
        }
        updateColumns() { this.updateAttribute("columns", this.model.columns, true); }
        updateParsedComputedColumns() { this.updateAttribute("parsed-computed-columns", this.model.parsed_computed_columns, true); }
        updateComputedColumns() { this.updateAttribute("computed-columns", this.model.computed_columns, true); }
        updateColumnPivots() { this.updateAttribute("column-pivots", this.model.column_pivots, true); }
        updateRowPivots() { this.updateAttribute("row-pivots", this.model.row_pivots, true); }
        updateAggregates() { this.updateAttribute("aggregates", this.model.row_pivots, true); }
        updateSort() { this.updateAttribute("sort", this.model.sort, true); }
        updateFilters() { this.updateAttribute("sort", this.model.filters, true); }
        updatePlugin() { this.updateAttribute("plugin", this.model.plugin, false); }
        updateTheme() {
            // When you update the class attribute you have to be carefull
            // For example when the user is dragging an element then 'dragging' is a part of the class attribute
            let old_class = this.perspective_element.getAttribute("class");
            let new_class = this.toNewClassAttribute(old_class, this.model.theme);
            this.perspective_element.setAttribute("class", new_class);
        }
        /** Helper function to generate the new class attribute string
         *
         * If old_class = 'perspective-viewer-material dragging' and theme = 'material-dark'
         * then 'perspective-viewer-material-dark dragging' is returned
         *
         * @param old_class For example 'perspective-viewer-material' or 'perspective-viewer-material dragging'
         * @param theme The name of the new theme. For example 'material-dark'
         */
        toNewClassAttribute(old_class, theme) {
            let new_classes = [];
            if (old_class != null) {
                new_classes = old_class.split(" ").filter(is_not_perspective_class);
            }
            new_classes.push(theme_to_class(theme));
            let new_class = new_classes.join(" ");
            return new_class;
        }
    }
    exports.PerspectiveViewerView = PerspectiveViewerView;
    PerspectiveViewerView.__name__ = "PerspectiveViewerView";
    // The Bokeh .ts model corresponding to the Bokeh .py model
    class PerspectiveViewer extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_PerspectiveViewer() {
            this.prototype.default_view = PerspectiveViewerView;
            this.define({
                source: [p.Any,],
                source_stream: [p.Any,],
                source_patch: [p.Any,],
                columns: [p.Array,],
                parsed_computed_columns: [p.Array, []],
                computed_columns: [p.Array,],
                column_pivots: [p.Array,],
                row_pivots: [p.Array,],
                aggregates: [p.Any,],
                sort: [p.Array,],
                filters: [p.Array,],
                plugin: [p.String,],
                theme: [p.String,],
            });
        }
    }
    exports.PerspectiveViewer = PerspectiveViewer;
    PerspectiveViewer.__name__ = "PerspectiveViewer";
    PerspectiveViewer.__module__ = "awesome_panel_extensions.bokeh_extensions.perspective_viewer";
    PerspectiveViewer.init_PerspectiveViewer();
},
"88538263fa": /* bokeh_extensions\shared.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    /** Function copied from the panel\models\layout.ts file of Panel
     * It is used for some models like deckgl, progress and vtlklayout
     * I have not yet understood why
     * @param el
     * @param model
     */
    function set_size(el, model) {
        let width_policy = model.width != null ? "fixed" : "fit";
        let height_policy = model.height != null ? "fixed" : "fit";
        const { sizing_mode } = model;
        if (sizing_mode != null) {
            if (sizing_mode == "fixed")
                width_policy = height_policy = "fixed";
            else if (sizing_mode == "stretch_both")
                width_policy = height_policy = "max";
            else if (sizing_mode == "stretch_width")
                width_policy = "max";
            else if (sizing_mode == "stretch_height")
                height_policy = "max";
            else {
                switch (sizing_mode) {
                    case "scale_width":
                        width_policy = "max";
                        height_policy = "min";
                        break;
                    case "scale_height":
                        width_policy = "min";
                        height_policy = "max";
                        break;
                    case "scale_both":
                        width_policy = "max";
                        height_policy = "max";
                        break;
                    default:
                        throw new Error("unreachable");
                }
            }
        }
        if (width_policy == "fixed" && model.width)
            el.style.width = model.width + "px";
        else if (width_policy == "max")
            el.style.width = "100%";
        if (height_policy == "fixed" && model.height)
            el.style.height = model.height + "px";
        else if (height_policy == "max")
            el.style.height = "100%";
    }
    exports.set_size = set_size;
    /** Transform the data of the cds to 'records' format, i.e. a list of objects
     *
     *  For example transforms to [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
     *
     *  Some js libraries like perspective-viewer uses this format to load data.
     *
     * @param cds
     */
    function transform_cds_to_records(cds) {
        const data = [];
        const columns = cds.columns();
        const cdsLength = cds.get_length();
        if (columns.length === 0 || cdsLength === null) {
            return [];
        }
        for (let i = 0; i < cdsLength; i++) {
            const item = {};
            for (const column of columns) {
                let array = cds.get_array(column);
                const shape = array[0].shape == null ? null : array[0].shape;
                if ((shape != null) && (shape.length > 1) && (typeof shape[0] == "number"))
                    item[column] = array.slice(i * shape[1], i * shape[1] + shape[1]);
                else
                    item[column] = array[i];
            }
            data.push(item);
        }
        return data;
    }
    exports.transform_cds_to_records = transform_cds_to_records;
    /** Helper function used to incrementally build a html element string
     *
     *  For example toAttribute("columns", ['x','y']) returns ' columns="['x','y']"
     *  For example toAttribute("columns", null) returns ""
     *
     * @param attribute
     * @param value
     */
    function toAttribute(attribute, value) {
        if (value === null) {
            return "";
        }
        if (typeof value !== "string") {
            value = JSON.stringify(value);
        }
        return " " + attribute + "='" + value + "'";
    }
    exports.toAttribute = toAttribute;
},
"eb1a40b8a7": /* bokeh_extensions\pivot_table.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    // Bokeh model for perspective-viewer
    // See https://github.com/finos/perspective/tree/master/packages/perspective-viewer
    // See https://docs.bokeh.org/en/latest/docs/reference/models/layouts.html
    const html_box_1 = require("@bokehjs/models/layouts/html_box");
    const dom_1 = require("@bokehjs/core/dom");
    // See https://docs.bokeh.org/en/latest/docs/reference/core/properties.html
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    const shared_1 = require("88538263fa") /* ./shared */;
    // The view of the Bokeh extension/ HTML element
    // Here you can define how to render the model as well as react to model changes or View events.
    class PivotTableView extends html_box_1.HTMLBoxView {
        connect_signals() {
            super.connect_signals();
            this.connect(this.model.source.properties.data.change, this.setData);
        }
        render() {
            super.render();
            this.container = dom_1.div({ class: "pnx-pivot-table" });
            shared_1.set_size(this.container, this.model);
            this.el.appendChild(this.container);
            this.setData();
        }
        setData() {
            console.log("setData");
            console.log(this.model.source.data);
            let data = shared_1.transform_cds_to_records(this.model.source);
            this.pivot_table_element = $(this.container);
            console.log(data);
            this.pivot_table_element.pivotUI(data, {});
        }
    }
    exports.PivotTableView = PivotTableView;
    PivotTableView.__name__ = "PivotTableView";
    // The Bokeh .ts model corresponding to the Bokeh .py model
    class PivotTable extends html_box_1.HTMLBox {
        constructor(attrs) {
            super(attrs);
        }
        static init_PivotTable() {
            this.prototype.default_view = PivotTableView;
            this.define({
                source: [p.Any,],
                source_stream: [p.Any,],
                source_patch: [p.Any,],
            });
        }
    }
    exports.PivotTable = PivotTable;
    PivotTable.__name__ = "PivotTable";
    PivotTable.__module__ = "awesome_panel_extensions.bokeh_extensions.pivot_table";
    PivotTable.init_PivotTable();
},
"cffb3837b7": /* bokeh_extensions\fast\fast_button.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    const button_1 = require("@bokehjs/models/widgets/button");
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    // Browse the fast-button api here  https://explore.fast.design/components/fast-button
    class FastButtonView extends button_1.ButtonView {
        _render_button(..._) {
            const button = document.createElement("fast-button");
            button.innerText = this.model.label;
            button.disabled = this.model.disabled;
            button.appearance = this.model.appearance;
            button.autofocus = this.model.autofocus;
            button.style.width = "100%";
            button.style.height = "100%";
            return button;
        }
    }
    exports.FastButtonView = FastButtonView;
    FastButtonView.__name__ = "FastButtonView";
    class FastButton extends button_1.Button {
        // __view_type__: FastButtonView
        constructor(attrs) {
            super(attrs);
        }
        static init_FastButton() {
            this.prototype.default_view = FastButtonView;
            this.define({
                appearance: [p.String,],
                autofocus: [p.Boolean,],
            });
        }
    }
    exports.FastButton = FastButton;
    FastButton.__name__ = "FastButton";
    FastButton.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_button";
    FastButton.init_FastButton();
},
"b5be3a3047": /* bokeh_extensions\fast\fast_checkbox_group.js */ function _(require, module, exports) {
    Object.defineProperty(exports, "__esModule", { value: true });
    const tslib_1 = require("tslib");
    const checkbox_group_1 = require("@bokehjs/models/widgets/checkbox_group");
    const mixins_1 = require("@bokehjs/styles/mixins");
    const inputs_1 = require("@bokehjs/styles/widgets/inputs");
    const dom_1 = require("@bokehjs/core/dom");
    const array_1 = require("@bokehjs/core/util/array");
    const p = tslib_1.__importStar(require("@bokehjs/core/properties"));
    // Browse the fast-button api here  https://explore.fast.design/components/fast-button
    class FastCheckboxGroupView extends checkbox_group_1.CheckboxGroupView {
        render() {
            // Cannot call super.render() as this will add the group twice
            // super.render()
            const group = dom_1.div({ class: [inputs_1.bk_input_group, this.model.inline ? mixins_1.bk_inline : null] });
            this.el.innerHTML = "";
            this.el.appendChild(group);
            const { active, labels } = this.model;
            this._inputs = [];
            for (let i = 0; i < labels.length; i++) {
                let fastCheckBox = document.createElement("fast-checkbox");
                if (this.model.readonly)
                    // Setting the property did not work for me. Thus I set the attribute
                    fastCheckBox.setAttribute("readonly", true);
                fastCheckBox.innerHTML = labels[i];
                const checkbox = fastCheckBox;
                checkbox.value = `${i}`;
                // const checkbox = input({type: `checkbox`, value: `${i}`})
                checkbox.addEventListener("change", () => this.change_active(i));
                this._inputs.push(checkbox);
                if (this.model.disabled)
                    checkbox.disabled = true;
                if (array_1.includes(active, i))
                    checkbox.checked = true;
                // const label_el = label({}, checkbox, span({}, labels[i]))
                group.appendChild(checkbox);
            }
        }
    }
    exports.FastCheckboxGroupView = FastCheckboxGroupView;
    FastCheckboxGroupView.__name__ = "FastCheckboxGroupView";
    class FastCheckboxGroup extends checkbox_group_1.CheckboxGroup {
        constructor(attrs) {
            super(attrs);
        }
        static init_FastCheckboxGroup() {
            this.prototype.default_view = FastCheckboxGroupView;
            this.define({
                readonly: [p.Boolean,],
            });
        }
    }
    exports.FastCheckboxGroup = FastCheckboxGroup;
    FastCheckboxGroup.__name__ = "FastCheckboxGroup";
    FastCheckboxGroup.__module__ = "awesome_panel_extensions.bokeh_extensions.fast.fast_checkbox_group";
    FastCheckboxGroup.init_FastCheckboxGroup();
},
}, "ed583be1cf", {"index":"ed583be1cf","bokeh_extensions/index":"f8ec988389","bokeh_extensions/web_component":"5c604c9068","bokeh_extensions/tabulator_model":"e2e34597ee","bokeh_extensions/perspective_viewer":"59f7dfa54f","bokeh_extensions/shared":"88538263fa","bokeh_extensions/pivot_table":"eb1a40b8a7","bokeh_extensions/fast/fast_button":"cffb3837b7","bokeh_extensions/fast/fast_checkbox_group":"b5be3a3047"}, {});
})

//# sourceMappingURL=awesome_panel_extensions.js.map
