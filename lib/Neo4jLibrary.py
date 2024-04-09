from neo4j import GraphDatabase, RoutingControl
from lib.ReadConfig import readConfig

initConfig = readConfig()

URI = initConfig['GraphDatabase']['uri']
AUTH = (initConfig['GraphDatabase']['username'], initConfig['GraphDatabase']['password'])
def neo4jGetTaxonomyLineage(ID, UpDown):
    childRelationship = '<-[:CHILD_OF*]-'
    if UpDown == "up":
        childRelationship = '-[:CHILD_OF*]->'
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            "MATCH (person_orig:Person {id: $id}) "
            f"OPTIONAL MATCH path = (person_orig){childRelationship}(person:Person)-[migration:MOVED_TO]->(location:Location) "
            "RETURN person.id, person.firstName, person.lastName, length(path) as degree, migration.date_raw, location.name, location.lat, location.lng "
            "UNION ALL "
            "MATCH (person:Person {id: $id})-[migration:MOVED_TO]->(location:Location) "
            "RETURN person.id, person.firstName, person.lastName, '0' as degree, migration.date_raw, location.name, location.lat, location.lng, person.summary "
            "ORDER BY person.id;",
            id=ID, childRelationship=childRelationship, database_="neo4j", routing_=RoutingControl.READ,
        )
    recordOutput = [list(record) for record in records if any(attribute is not None for attribute in record)]
    Output = [[value if value is not None else '' for value in inner] for inner in recordOutput]
    # print(recordOutput)
    # print(len(recordOutput))
    return Output


def neo4jGetTaxonomyLastname(ID,lastName):
    query = (
        "MATCH (people:Person)-[migration:MOVED_TO]->(location:Location) "
        + ("WHERE people.lastName = $lastName " if lastName else "")
        + "RETURN people.id, people.firstName, people.lastName, NULL as SomeColumn, migration.date_raw, location.name, location.lat, location.lng, people.summary "
        + "ORDER BY people.id"
    )
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            query,
            lastName=lastName, database_="neo4j", routing_=RoutingControl.READ,
        )
    recordOutput = [list(record) for record in records if any(attribute is not None for attribute in record)]
    Output = [[value if value is not None else '' for value in inner] for inner in recordOutput]
    # print(recordOutput)
    # print(len(recordOutput))
    return Output


def neo4jGetPeopleList():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            "MATCH (p:Person) "
            "OPTIONAL MATCH (p)-[:CHILD_OF]->(p_parent:Person) "
            "WITH p, COLLECT(p_parent.firstName + ' ' + p_parent.lastName) AS parentNames "
            "RETURN p.id AS personID, p.firstName AS personFirstName, p.lastName AS personLastName, parentNames;",
            database_="neo4j", routing_=RoutingControl.READ,
        )
    records = [list(record) for record in records if any(attribute is not None for attribute in record)]
    recordOutput = [[*record[:3], ','.join(record[3])] for record in records]
    Output = [[value if value is not None else '' for value in inner] for inner in recordOutput]
    # print(Output)
    # print("neo4jGetPeopleList",len(Output))
    return Output



# neo4jGetTaxonomyLineage('262004747968', 'down')
# getTaxonomyLastName('Kirkpatrick')
# neo4jGetPeopleList()


# (262004748032, 'Mary', 'Guthrie', "Robert 'Guttery' Guthrie,Elizabeth Jane Caldwell")









	
