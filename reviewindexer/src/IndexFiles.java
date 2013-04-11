

//import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.IndexWriter;
//import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.IndexWriterConfig;
//import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

//import java.io.BufferedReader;
import java.io.File;
//import java.io.FileInputStream;
//import java.io.FileNotFoundException;
//import java.io.IOException;
//import java.io.InputStreamReader;
import java.sql.*;
//import java.util.Date;


public class IndexFiles {
	final static String indexPath = "index";

	private IndexFiles() {}

	public static void main (String[] args) {
		try {
			Directory dir = FSDirectory.open(new File(indexPath));
			Class.forName("com.mysql.jdbc.Driver").newInstance();
			Connection conn = DriverManager.getConnection("jdbc:mysql://localhost/reviews", "root", "");
			StandardAnalyzer analyzer = new StandardAnalyzer(Version.LUCENE_42);
			IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_42, analyzer);
			IndexWriter writer = new IndexWriter(dir, iwc);
			System.out.println("Indexing to directory '" + indexPath + "'...");
			indexDocs(writer, conn);
			writer.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	static void indexDocs(IndexWriter writer, Connection conn) throws Exception {
		String sql = "select * from reviews";
		Statement stmt = conn.createStatement();
		ResultSet rs = stmt.executeQuery(sql);
		while (rs.next()) {
			Document d = new Document();
			d.add(new LongField("id", rs.getLong("id"), Field.Store.YES));
			d.add(new TextField("reviewtext", rs.getString("reviewtext"), Field.Store.NO));
			writer.addDocument(d);
		}
	}
}
