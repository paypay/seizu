import { createStyles, makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) =>
  createStyles({
    '@global': {
      '*': {
        boxSizing: 'border-box',
        margin: 0,
        padding: 0
      },
      html: {
        '-webkit-font-smoothing': 'antialiased',
        '-moz-osx-font-smoothing': 'grayscale'
      },
      body: {
        backgroundColor: '#f4f6f8',
        height: '100%',
        width: '100%'
      },
      a: {
        color: theme.palette.primary.main,
        textDecoration: 'none'
      },
      '#root': {
        height: '100%',
        width: '100%'
      },
      // Update CSS for markdoc, which places nodes under "article" nodes
      'article ol': {
        paddingLeft: 40,
        paddingTop: 10,
        paddingBottom: 10
      },
      'article ul': {
        paddingLeft: 40,
        paddingTop: 10,
        paddingBottom: 10
      },
      'article h1': {
        fontWeight: 500,
        fontSize: 29,
        letterSpacing: '-0.24px'
      },
      'article h2': {
        fontWeight: 500,
        fontSize: 24,
        letterSpacing: '-0.06px'
      },
      'article h3': {
        fontWeight: 500,
        fontSize: 20,
        letterSpacing: '-0.05px'
      },
      'article h4': {
        fontWeight: 500,
        fontSize: 16,
        letterSpacing: '-0.05px'
      },
      'article h5': {
        fontWeight: 500,
        fontSize: 16,
        letterSpacing: '-0.05px'
      },
      'article h6': {
        fontWeight: 500,
        fontSize: 14,
        letterSpacing: '-0.05px'
      }
    }
  })
);

function GlobalStyles() {
  useStyles();

  return null;
}

export default GlobalStyles;
