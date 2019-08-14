import React, {Component} from 'react';
import ReactHtmlParser from 'react-html-parser';
import PropTypes from 'prop-types';


/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */
export default class Svg extends Component {
  constructor(props) {
    super(props)

    this.svgRef = React.createRef();
    this.state = {svgjsx: ""};
  }

  render() {
    const {id, classMap, setProps, value} = this.props;
    
    const svgtag = ReactHtmlParser(value)[0];
    console.log(svgtag);
    svgtag.props.viewBox = svgtag.props.viewbox;
    
    let recurseNodes = (node) => {
      if(node == null || node.props == null) {
        return;
      }
      if(node.props.id != null && classMap.hasOwnProperty(node.props.id)) {
        node.props.className = classMap[node.props.id];
      }
      let children = React.Children.toArray(node.props.children)
      React.Children.forEach(node.props.children, recurseNodes);
    }
    console.log(svgtag)
    console.log(classMap)
    
    recurseNodes(svgtag);

    return svgtag;
  }
}

Svg.defaultProps = {};

Svg.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks
   */
  id: PropTypes.string,

  /**
   * The value displayed in the input
   */
  value: PropTypes.string.isRequired,

  /**
   * A map of ids and the classes to be set on them for controlling
   * the inner svg element classes
   */
  classMap: PropTypes.object.isRequired,

  /**
   * Dash-assigned callback that should be called whenever any of the
   * properties change
   */
  setProps: PropTypes.func
};
