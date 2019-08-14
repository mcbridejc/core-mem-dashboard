# AUTO GENERATED FILE - DO NOT EDIT

svg <- function(id=NULL, value=NULL, classMap=NULL) {
    
    props <- list(id=id, value=value, classMap=classMap)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Svg',
        namespace = 'svg',
        propNames = c('id', 'value', 'classMap'),
        package = 'svg'
        )

    structure(component, class = c('dash_component', 'list'))
}
