import React from 'react'
import Button from 'react-bootstrap/Button'
import ButtonGroup from 'react-bootstrap/ButtonGroup'

class PageNavigator extends React.Component {
  constructor(props) {
    super(props)
  }

  canMoveNextPage = () => (this.props.nextPageUrl !== null)

  canMovePrevPage = () => (this.props.prevPageUrl !== null)

  moveNextPage = () => {
    if (this.canMoveNextPage()) {
      console.log(this.props.nextPageUrl)
      this.props.onChangePage(this.props.nextPageUrl)
    }
  }

  movePrevPage = () => {
    if (this.canMovePrevPage()) {
      this.props.onChangePage(this.props.prevPageUrl)
    }
  }

  render() {
    return (
      <ButtonGroup id='page_navigator' aria-label='Page Navigator'>
        <Button
          variant='primary'
          onClick={this.movePrevPage}
          disabled={!this.canMovePrevPage()}
        >
          Prev Page
        </Button>
        <Button
          variant='primary'
          onClick={this.moveNextPage}
          disabled={!this.canMoveNextPage()}
        >
          Next Page
        </Button>
      </ButtonGroup>
    )
  }
}

export default PageNavigator