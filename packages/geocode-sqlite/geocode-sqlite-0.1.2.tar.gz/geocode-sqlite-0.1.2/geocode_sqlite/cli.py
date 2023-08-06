import click

from geopy import geocoders
from sqlite_utils import Database

from .utils import geocode_table


@click.group()
@click.version_option()
@click.argument(
    "database",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.argument("table", type=click.STRING)
@click.option("-l", "--location", type=click.STRING, default="{location}")
@click.option("-d", "--delay", type=click.FLOAT, default=1.0)
@click.option("--latitude", type=click.STRING, default="latitude")
@click.option("--longitude", type=click.STRING, default="longitude")
def cli(database, table, location, delay, latitude, longitude):
    "Geocode rows from a SQLite table"


@cli.resultcallback()
def geocode(geocoder, database, table, location, delay, latitude, longitude):
    "Do the actual geocoding"
    click.echo(f"Geocoding table {table} using {geocoder.__class__.__name__}")
    if latitude != "latitude":
        click.echo(f"Using custom latitude field: {latitude}")

    if longitude != "longitude":
        click.echo(f"Using custom longitude field: {longitude}")

    count = geocode_table(
        database,
        table,
        geocoder,
        query_template=location,
        delay=delay,
        latitude_column=latitude,
        longitude_column=longitude,
    )
    click.echo("Geocoded {} rows".format(count))


@cli.command("test")
@click.option("-p", "--db-path", type=click.Path(exists=True))
def use_tester(db_path):
    "Use the dummy geocoder for testing"
    click.echo(f"Using test geocoder with database {db_path}")
    from .testing import DummyGeocoder

    return DummyGeocoder(Database(db_path))


@cli.command("bing")
@click.option(
    "-k", "--api-key", type=click.STRING, required=True, envvar="BING_API_KEY"
)
def bing(api_key):
    click.echo("Using Bing geocoder")
    return geocoders.Bing(api_key=api_key)


@cli.command("googlev3")
@click.option(
    "-k", "--api-key", type=click.STRING, required=True, envvar="GOOGLE_API_KEY"
)
@click.option("--domain", type=click.STRING, default="maps.googleapis.com")
def google(api_key, domain):
    click.echo(f"Using GoogleV3 geocoder at domain {domain}")
    return geocoders.GoogleV3(api_key=api_key, domain=domain)


@cli.command("mapquest")
@click.option(
    "-k", "--api-key", type=click.STRING, required=True, envvar="MAPQUEST_API_KEY"
)
def mapquest(api_key):
    click.echo("Using MapQuest geocoder")
    return geocoders.MapQuest(api_key=api_key)


@cli.command()
@click.option("--user-agent", type=click.STRING)
@click.option("--domain", type=click.STRING, default="nominatim.openstreetmap.org")
def nominatum(user_agent, domain):
    click.echo(f"Using Nominatum geocoder at {domain}")
    return geocoders.Nominatim(user_agent=user_agent, domain=domain)


@cli.command("open-mapquest")
@click.option(
    "-k", "--api-key", type=click.STRING, required=True, envvar="MAPQUEST_API_KEY"
)
def open_mapquest(api_key):
    click.echo("Using MapQuest geocoder")
    return geocoders.MapQuest(api_key=api_key)

