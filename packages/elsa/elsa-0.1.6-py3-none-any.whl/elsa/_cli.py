import os
import sys
import urllib.parse
import warnings

from flask import Response
import flask_frozen
import click

from ._deployment import deploy as deploy_
from ._shutdown import ShutdownableFreezer, inject_shutdown


def port_option():
    return click.option(
        '--port', type=int, default=8003,
        help='Port to listen at')


def cname_option():
    return click.option(
        '--cname/--no-cname', default=True,
        help='Whether to create the CNAME file, default is to create it')


def path_option(app):
    return click.option(
        '--path', default=os.path.join(app.root_path, '_build'),
        help='Input path, default _build')


def verbose_option():
    return click.option(
        '-v/-q', '--verbose/--quiet',
        help='Print out page URLs as they are frozen')


def host_option():
    return click.option(
        '--host',
        help='Host to listen at when serving')


def freeze_app(app, freezer, path, base_url, verbose):
    if not base_url:
        raise click.UsageError('No base URL provided, use --base-url')
    print('Generating HTML...')
    app.config['FREEZER_DESTINATION'] = path
    app.config['FREEZER_BASE_URL'] = base_url
    app.config['SERVER_NAME'] = urllib.parse.urlparse(base_url).netloc

    # make sure Frozen Flask warnings are treated as errors
    warnings.filterwarnings('error', category=flask_frozen.FrozenFlaskWarning)

    try:
        for page in freezer.freeze_yield():
            if verbose:
                print('Frozen', page.url, file=sys.stderr)
    except flask_frozen.FrozenFlaskWarning as w:
        print('Error:', w, file=sys.stderr)
        sys.exit(1)


def inject_cname(app):
    """Create CNAME route for GitHub pages"""
    @app.route('/CNAME')
    def cname():
        return Response(app.config['SERVER_NAME'],
                        mimetype='application/octet-stream')


def cli(app, *, freezer=None, base_url=None, invoke_cli=True):
    """ Generates command-line interface for the provided app.

    If ``invoke_cli`` is set to ``True`` (the default),
    the cli is invoked right away,
    otherwise it's returned so it can be used further.
    """
    if not freezer:
        freezer = ShutdownableFreezer(app)

    @click.group(context_settings=dict(help_option_names=['-h', '--help']),
                 help=__doc__)
    def command():
        pass

    @command.command()
    @port_option()
    @cname_option()
    @host_option()
    def serve(port, cname, host):
        """Run a debug server"""

        # Workaround for https://github.com/pallets/flask/issues/1907
        auto_reload = app.config.get('TEMPLATES_AUTO_RELOAD')
        if auto_reload or auto_reload is None:
            app.jinja_env.auto_reload = True

        inject_shutdown(app)
        if cname:
            inject_cname(app)

        kwargs = {}
        if host is not None:
            kwargs['host'] = host

        app.run(port=port, debug=True, **kwargs)

    @command.command()
    @path_option(app)
    @click.option('--base-url', default=base_url,
                  help='URL for the application, used for external links, ' +
                  ('default {}'.format(base_url) if base_url else 'mandatory'))
    @click.option('--serve/--no-serve',
                  help='After building the site, run a server with it')
    @verbose_option()
    @port_option()
    @cname_option()
    @host_option()
    def freeze(path, base_url, serve, port, cname, verbose, host):
        """Build a static site"""
        if cname:
            inject_cname(app)

        freeze_app(app, freezer, path, base_url, verbose=verbose)

        kwargs = {}
        if host is not None:
            kwargs['host'] = host

        if serve:
            freezer.serve(port=port, **kwargs)

    @command.command()
    @path_option(app)
    @click.option('--base-url', default=base_url,
                  help='URL for the application, used for external links, ' +
                  ('default {}'.format(base_url) if base_url else 'mandatory'
                   ' with --freeze'))
    @click.option('--remote', default='origin',
                  help='The name of the remote to push to, '
                  'default origin')
    @click.option('--push/--no-push', default=None,
                  help='Whether to push the gh-pages branch, '
                  'deprecated default is to push')
    @click.option('--freeze/--no-freeze', default=True,
                  help='Whether to freeze the site before deploying, '
                  'default is to freeze')
    @click.option('--show-git-push-stderr', is_flag=True,
                  help='Show the stderr output of `git push` failure, '
                       'might be dangerous if logs are public')
    @verbose_option()
    @cname_option()
    def deploy(path, base_url, remote, push, freeze,
               show_git_push_stderr, cname, verbose):
        """Deploy the site to GitHub pages"""
        if push is None:
            warnings.simplefilter('always')
            msg = ('Using deploy without explicit --push/--no-push is '
                   'deprecated. Assuming --push for now. In future versions '
                   'of elsa, the deploy command will not push to the remote '
                   'server by default. Use --push explicitly to maintain '
                   'current behavior.')
            warnings.warn(msg, DeprecationWarning)
            push = True
        if freeze:
            if cname:
                inject_cname(app)
            freeze_app(app, freezer, path, base_url, verbose=verbose)

        deploy_(path, remote=remote, push=push, show_err=show_git_push_stderr)

    if invoke_cli:
        return command()
    else:
        return command
