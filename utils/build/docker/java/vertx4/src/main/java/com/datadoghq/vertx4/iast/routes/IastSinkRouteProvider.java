package com.datadoghq.vertx4.iast.routes;

import com.datadoghq.system_tests.iast.utils.*;
import io.vertx.core.http.HttpServerRequest;
import io.vertx.core.json.Json;
import io.vertx.ext.web.Router;
import io.vertx.ext.web.handler.BodyHandler;

import javax.naming.directory.InitialDirContext;
import javax.sql.DataSource;
import java.util.function.Consumer;

public class IastSinkRouteProvider implements Consumer<Router> {

    private final DataSource dataSource;
    private final InitialDirContext ldapContext;

    public IastSinkRouteProvider(final DataSource dataSource, final InitialDirContext ldapContext) {
        this.dataSource = dataSource;
        this.ldapContext = ldapContext;
    }

    @Override
    public void accept(final Router router) {
        final String superSecretAccessKey = "insecure";
        final CmdExamples cmd = new CmdExamples();
        final CryptoExamples crypto = new CryptoExamples();
        final LDAPExamples ldap = new LDAPExamples(ldapContext);
        final PathExamples path = new PathExamples();
        final SqlExamples sql = new SqlExamples(dataSource);
        final WeakRandomnessExamples weakRandomness = new WeakRandomnessExamples();

        router.route("/iast/*").handler(BodyHandler.create());

        router.get("/iast/insecure_hashing/deduplicate").handler(ctx ->
                ctx.response().end(crypto.removeDuplicates(superSecretAccessKey))
        );
        router.get("/iast/insecure_hashing/multiple_hash").handler(ctx ->
                ctx.response().end(crypto.multipleInsecureHash(superSecretAccessKey))
        );
        router.get("/iast/insecure_hashing/test_secure_algorithm").handler(ctx ->
                ctx.response().end(crypto.secureHashing(superSecretAccessKey))
        );
        router.get("/iast/insecure_hashing/test_md5_algorithm").handler(ctx ->
                ctx.response().end(crypto.insecureMd5Hashing(superSecretAccessKey))
        );
        router.get("/iast/insecure_cipher/test_secure_algorithm").handler(ctx ->
                ctx.response().end(crypto.secureCipher(superSecretAccessKey))
        );
        router.get("/iast/insecure_cipher/test_insecure_algorithm").handler(ctx ->
                ctx.response().end(crypto.insecureCipher(superSecretAccessKey))
        );
        router.post("/iast/sqli/test_insecure").handler(ctx -> {
            final HttpServerRequest request = ctx.request();
            final String username = request.getParam("username");
            final String password = request.getParam("password");
            ctx.response().end(Json.encodeToBuffer(sql.insecureSql(username, password)));
        });
        router.post("/iast/sqli/test_secure").handler(ctx -> {
            final HttpServerRequest request = ctx.request();
            final String username = request.getParam("username");
            final String password = request.getParam("password");
            ctx.response().end(Json.encodeToBuffer(sql.secureSql(username, password)));
        });
        router.post("/iast/ldapi/test_insecure").handler(ctx -> {
            final HttpServerRequest request = ctx.request();
            final String username = request.getParam("username");
            final String password = request.getParam("password");
            ctx.response().end(ldap.injection(username, password));
        });
        router.post("/iast/ldapi/test_secure").handler(ctx -> ctx.response().end(ldap.secure()));
        router.post("/iast/cmdi/test_insecure").handler(ctx -> {
            final HttpServerRequest request = ctx.request();
            final String cmdParam = request.getParam("cmd");
            ctx.response().end(cmd.insecureCmd(cmdParam));
        });
        router.post("/iast/path_traversal/test_insecure").handler(ctx -> {
            final HttpServerRequest request = ctx.request();
            final String pathParam = request.getParam("path");
            ctx.response().end(path.insecurePathTraversal(pathParam));
        });
        router.get("/iast/weak_randomness/test_insecure").handler(ctx ->
                ctx.response().end(weakRandomness.weakRandom())
        );
        router.get("/iast/weak_randomness/test_secure").handler(ctx ->
                ctx.response().end(weakRandomness.secureRandom())
        );
        router.post("/iast/unvalidated_redirect/test_insecure_forward").handler(ctx ->{
                    final HttpServerRequest request = ctx.request();
                    final String location = request.getParam("location");
                    ctx.reroute(location);
                }
        );
        router.post("/iast/unvalidated_redirect/test_secure_forward").handler(ctx ->
                ctx.reroute("http://dummy.location.com")
        );
        router.post("/iast/unvalidated_redirect/test_insecure_header").handler(ctx ->
                {
                    final HttpServerRequest request = ctx.request();
                    final String location = request.getParam("location");
                    ctx.response().putHeader("Location", location).end();
                }
        );
        router.post("/iast/unvalidated_redirect/test_secure_header").handler(ctx ->
                ctx.response().putHeader("Location", "http://dummy.location.com").end()
        );
        router.post("/iast/unvalidated_redirect/test_insecure_redirect").handler(ctx ->
                {
                    final HttpServerRequest request = ctx.request();
                    final String location = request.getParam("location");
                    ctx.redirect(location);
                }
        );
        router.post("/iast/unvalidated_redirect/test_secure_redirect").handler(ctx ->
                ctx.redirect("http://dummy.location.com")
        );
    }
}
