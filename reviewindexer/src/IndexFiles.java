//import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
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
	final static String indexPath = "../index";

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
			int num = indexDocs(writer, conn);
			writer.close();
			System.out.println("Indexed " + num + " documents.");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private static int indexDocs(IndexWriter writer, Connection conn) throws Exception {
		String sql = "select * from reviews";
		Statement stmt = conn.createStatement();
		ResultSet rs = stmt.executeQuery(sql);
		int i = 0;
		while (rs.next()) {
			Document d = new Document();
			d.add(new IntField("id", rs.getInt("id"), Field.Store.YES));
			d.add(new TextField("reviewtext", rs.getString("reviewtext"), Field.Store.NO));
			d.add(new StringField("name", rs.getString("name"), Field.Store.NO));
			writer.addDocument(d);
			++i;
		}
		return i;
	}
}
