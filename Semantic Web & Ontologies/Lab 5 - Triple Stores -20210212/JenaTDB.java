import java.io.InputStream;
import java.util.*;
import org.apache.jena.graph.Graph;
import org.apache.jena.graph.GraphListener;
import org.apache.jena.graph.Node;
import org.apache.jena.graph.NodeFactory;
import org.apache.jena.graph.Triple;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.apache.jena.rdf.model.ResourceFactory;
import org.apache.jena.sparql.core.Quad;
import org.apache.jena.sparql.util.graph.GraphListenerBase;
import org.apache.jena.tdb.TDBFactory;
import org.apache.jena.tdb.TDBLoader;
import org.apache.jena.tdb.store.DatasetGraphTDB;
import org.apache.jena.tdb.sys.TDBInternal;
import org.apache.jena.util.FileManager;
import org.apache.jena.vocabulary.RDFS;
import org.apache.jena.rdf.model.*;
import org.apache.jena.query.Dataset;
import org.apache.jena.query.ReadWrite;
import org.apache.jena.tdb.base.file.Location;

import org.apache.jena.query.Dataset;
import org.apache.jena.query.ReadWrite;
import org.apache.jena.query.Query ;
import org.apache.jena.query.QueryExecution ;
import org.apache.jena.query.QueryExecutionFactory ;
import org.apache.jena.query.QueryFactory ;
import org.apache.jena.query.QuerySolution ;
import org.apache.jena.query.ResultSet ;

public class JenaTDB {
	
// Methode à n'executer qu'une seule fois : lors de la création du dataset 
	
public Dataset createDataset(String file, String directory)
{
	try{
		Dataset dataset = TDBFactory.createDataset(directory);
		dataset.begin(ReadWrite.WRITE) ;
		Model model = dataset.getDefaultModel();
		TDBLoader.loadModel(model, file);
		dataset.commit();
		dataset.end();
		return dataset;
	}catch(Exception ex)
	{
		System.out.println("##### Error Fonction: createDataset #####");
		System.out.println(ex.getMessage());
		return null;
	}
}

public void readDataset(String directory)
{
	
	Dataset d = TDBFactory.createDataset(directory);
	Model model = d.getDefaultModel();
	
	d.begin(ReadWrite.READ);
	try {
		Iterator<Quad> iter = d.asDatasetGraph().find();
		int i=0;
		System.out.println("begin ");
		while (iter.hasNext() && i < 10) {
			Quad quad = iter.next();
			System.out.println("iteration "+i);
			System.out.println(quad);
			i++;
	 }
	} finally { d.end(); }
		d.close();
		System.out.println("finish ...");
}

public void queryDataset(String directory) {

Dataset d = TDBFactory.createDataset(directory);
Model model = d.getDefaultModel();

String sparqlQueryString = "SELECT (count(*) AS ?count) { ?s ?p ?o }" ;

//See http://incubator.apache.org/jena/documentation/query/app_api.html

Query query = QueryFactory.create(sparqlQueryString) ;
QueryExecution qexec = QueryExecutionFactory.create(query, d) ;
	
try {
		ResultSet results = qexec.execSelect() ;
		for ( ; results.hasNext() ; )
			{
			QuerySolution soln = results.nextSolution() ;
			int count = soln.getLiteral("count").getInt() ;
			System.out.println("count = "+count) ;
		}
	} finally { qexec.close() ; }
		
	//Close the dataset.
	d.close();
}

public void complexQueryDataset(String directory) {

Dataset d = TDBFactory.createDataset(directory);
Model model = d.getDefaultModel();
	
	
/*String sparqlQueryString ="PREFIX humans:<http://www.inria.fr/2007/09/11/humans.rdfs#>" +
						   "PREFIX inst:<http://www.inria.fr/2007/09/11/humans.rdfs-instances#> " +
						   "SELECT ?x WHERE {?x humans:hasSpouse inst:Catherine .}";*/

String sparqlQueryString ="PREFIX humans:<http://www.inria.fr/2007/09/11/humans.rdfs#>" +
		   "PREFIX inst:<http://www.inria.fr/2007/09/11/humans.rdfs-instances#> " +
		   "SELECT ?x ?y WHERE {?x humans:hasSpouse ?y .}";
// See http://incubator.apache.org/jena/documentation/query/app_api.html

Query query = QueryFactory.create(sparqlQueryString) ;
QueryExecution qexec = QueryExecutionFactory.create(query, d) ;
	try {
	ResultSet results = qexec.execSelect() ;
	while (results.hasNext()) {
		QuerySolution sol = results.next();
		System.out.println("Solution := "+sol);
		for (Iterator<String> names = sol.varNames(); names.hasNext(); ) {
		final String name = names.next();
		System.out.println("\t"+name+" := "+sol.get(name));
	 }
	}
	} finally { qexec.close() ; }
	// Close the dataset.
	d.close();
}

public static void main(String [] args) {
	String file = "/Users/fatihasais/Dropbox/1-MyData/1-Enseignements/1-IUT/2-cours/2-BDR-PRISM/2020/Jena-TDB/human_2007_09_11.rdf";
	String directory ="/Users/fatihasais/Dropbox/1-MyData/1-Enseignements/1-IUT/2-cours/2-BDR-PRISM/2020/Jena-TDB/dir1";
	JenaTDB jtdb = new JenaTDB(); 
	
	// création du dataset /!\ à faire qu'une seule fois 
	//Dataset d = jtdb.createDataset(file, directory);
	//jtdb.readDataset(directory);
	jtdb.complexQueryDataset(directory);
	

}

}// Class
